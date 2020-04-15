import requests
import threading
import json

from django.db.models import F


from .wallet_service import *
from .node_service import *
from .accounts import *
from ._pow import POWService
from ..common.retry import retry


logger = logging.getLogger(__name__)

class AccountBalanceMismatchException(Exception):
    def __init__(self, balance_actual, balance_db, account):
        Exception.__init__(self, "{0} != {1} for account: {2}".format(balance_actual, balance_db, account))

class InsufficientNanoException(Exception):
    def __init__(self):
        Exception.__init__(self, "The Nano account did not have enough RAW to make a transaction.")

class AddressDoesNotExistException(Exception):
    def __init__(self, account, wallet):
        Exception.__init__(self, "The Nano address {0} does not exist on wallet {1}".format(account, wallet))

class NoIncomingBlocksException(Exception):
    def __init__(self, account):
        Exception.__init__(self, "There were no incoming blocks to receive for the account: %s." % account)

class TooManyIncomingBlocksException(Exception):
    def __init__(self, account):
        Exception.__init__(self, "There were more than one incoming blocks for the account: %s." % account)

class InvalidPOWException(Exception):
    def __init__(self):
        Exception.__init__(self, "The POW on the account was not valid.")

class NoAccountsException(Exception):
    def __init__(self, node='NA'):
        Exception.__init__(self, "The specified node (%s) does not have any accounts." % node)

def new_transaction(origin_account, destination_account, amount, batch):
    """
    Create a transaction from the given properties.
    We must lock accounts on creation of transaction between them.

    @param origin_account: Account source
    @param destination_account: Account receiver
    @param amount: Amount in RAW to send
    @param batch: Batch of the transaction
    @return: New transaction object
    """

    if amount < 0:
        logger.exception("Cannot send negative amount %s." % amount)
        raise ValueError("Amount sent must be positive.")

    ##Lock origin and destination accounts
    ##Unlock accounts
    origin_account.lock()
    destination_account.lock()

    transaction = models.Transaction(
        origin=origin_account,
        destination=destination_account,
        amount=amount,
        batch=batch
    )

    retry(lambda: transaction.save())

    return transaction

def send_transaction(transaction):
    """
    Complete a transaction on the Nano network while timing results.
    We must unlock accounts on any failure or at completion of sending.

    @param transaction: Transaction to execute
    @return: Transaction object with new information
    @raise: RPCException: RPC Failure
    @raise: AccountBalanceMismatchException: Will prevent the execution of the current transaction but will also rebalance the account
    @raise: InsufficientNanoException: The origin account does not have enough funds
    @raise: InvalidPOWException: The origin account does not have valid POW
    @raise: NoIncomingBlocksException: Incoming block not found on destination node. This will lead to invalid POW and balance in the destination account if not handled
    @raise: TooManyIncomingBlocksException: Incoming block not found on destination node. This will lead to invalid POW and balance in the destination account if not handled
    """

    rpc_origin_node = nano.rpc.Client(transaction.origin.wallet.node.URL)
    rpc_destination_node = nano.rpc.Client(transaction.destination.wallet.node.URL)

    if (transaction.origin.current_balance - transaction.amount < 0):
        ##Unlock accounts
        transaction.origin.unlock()
        transaction.destination.unlock()
        logger.info("InsufficientNanoException %s" % transaction.origin.address)
        raise InsufficientNanoException()

    transaction.PoW_cached_send = True
    pre_validation_work = transaction.origin.POW

    if not validate_or_regenerate_PoW(transaction.origin):
        logger.error('Total faliure of dPoW. Aborting transaction account %s' % transaction.origin.address)
        transaction.origin.unlock()
        transaction.destination.unlock()
        raise InvalidPOWException()

    transaction.origin = get_account(transaction.origin.address)

    if not pre_validation_work == transaction.origin.POW:
        transaction.PoW_cached_send = False

    try:
        logger.info("Transaction for send block status before_send")
        account_info = retry(lambda: rpc_origin_node.account_info(transaction.origin.address, representative=True))
        time_before = int(round(time.time() * 1000))

        sent_done, hash_value = create_and_process(transaction, account_info, "send")

        if not sent_done:
            logger.error("Error in create and process send")
            raise nano.rpc.RPCException()

        time_after = int(round(time.time() * 1000))
        roundtrip_time = time_after - time_before

        # Start timing once block is published to node and account for time on trip back
        transaction.start_send_timestamp = int(round(time.time() * 1000)) - (roundtrip_time * .75)

        logger.info("Transaction in status send to node %s " % transaction.transaction_hash_sending)
        transaction.POW_send = transaction.origin.POW

        # Update the balances and POW
        transaction.origin.current_balance = transaction.origin.current_balance - transaction.amount
        transaction.destination.current_balance = transaction.destination.current_balance + transaction.amount
        transaction.origin.POW = None

    except nano.rpc.RPCException as e:
        logger.exception("RPCException one %s" % e)
        transaction.origin.unlock()
        transaction.destination.unlock()
        raise nano.rpc.RPCException()

    retry(lambda: transaction.origin.save())
    retry(lambda: transaction.destination.save())
    retry(lambda: transaction.save())

    # Return as soon as transaction_hash_receiving is available
    # Finish work on 2nd thread
    t = threading.Thread(target=send_receive_block_async, args=(transaction, rpc_destination_node))
    t.start()

    # Regenerate PoW
    POWService.enqueue_account(address=transaction.origin.address, frontier=transaction.transaction_hash_sending)
    return transaction


def send_receive_block_async(transaction, rpc_destination_node):
    """
    Receive funds on managed account.

    @param transaction: Managed transaction
    """

    transaction.PoW_cached_send = True
    pre_validation_work = transaction.destination.POW
    if not validate_or_regenerate_PoW(transaction.destination):
        logger.error('Total failure of dPoW. Aborting transaction account %s' % transaction.destination.address)
        transaction.origin.unlock()
        transaction.destination.unlock()
        raise InvalidPOWException()

    transaction.destination = get_account(transaction.destination.address)

    if not pre_validation_work == transaction.destination.POW:
        transaction.PoW_cached_send = False

    try:
        logger.info("Transaction for receive block status before_receive")
        account_info = retry(lambda: rpc_destination_node.account_info(transaction.destination.address, representative=True))
        time_before = int(round(time.time() * 1000))

        ##Create and process block work around
        receive_done, hash_value = create_and_process(transaction, account_info, "receive")
        if not receive_done:
            logger.exception("Error in create and process receive")
            raise nano.rpc.RPCException()

        time_after = int(round(time.time() * 1000))

        roundtrip_time = time_after - time_before
        transaction.start_receive_timestamp = int(round(time.time() * 1000)) - (roundtrip_time * .75)

        transaction.POW_receive = transaction.destination.POW
    except nano.rpc.RPCException as e:
        ##Unlock accounts
        logger.exception("RPCException two %s" % e)

        transaction.origin.unlock()
        transaction.destination.unlock()

        transaction.destination.POW = None
        frontier = retry(lambda: rpc_destination_node.frontiers(account=transaction.destination.address, count=1)[transaction.destination.address])
        POWService.enqueue_account(address=transaction.destination.address, frontier=frontier)

        raise nano.rpc.RPCException()

    transaction.transaction_hash_receiving = hash_value
    transaction.destination.POW = None

    retry(lambda: transaction.destination.save())
    retry(lambda: transaction.save())
    POWService.enqueue_account(address=transaction.destination.address, frontier=transaction.transaction_hash_receiving)


def get_transactions(enabled=True, batch=None, download=False):
    """
    Get all transactions in the database.

    @param enabled: Get transactions whose origin and destination node is enabled
    @param batch: If not None, only get transactions within a batch (precedence)
    @return: Query of all transactions
    """

    if batch is not None:
        return retry(lambda: models.Transaction.objects.filter(batch__id=batch.id))

    if enabled:
        return retry(lambda: models.Transaction.objects.filter(origin__wallet__node__enabled=enabled, destination__wallet__node__enabled=enabled))

    if download:
        return retry(lambda: models.Transaction.objects.select_related().order_by('-id')[:])

    return retry(lambda: models.Transaction.objects.all())


def get_recent_transactions(count=25):
    """
    Get most recent count transaction with enabled nodes

    @param count: Number of most recent transactions to return
    @return: Query of transactions
    """
    return retry(lambda: models.Transaction.objects.filter(end_send_timestamp__gt=(F('start_send_timestamp')+180)).select_related().order_by('-id')[:count])


def get_transaction(id):
    """
    Get a transaction by id

    @param id: Id of the transaction to search for
    @return: None if not found or Transaction object
    @raise: MultipleObjectsReturned: If more than one object exists, this is raised
    """

    try:
        return retry(lambda: models.Transaction.objects.get(id=id))
    except models.Transaction.DoesNotExist:
        return None
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned()


def create_and_process(transaction, account_info, type):

    if not type == "receive" and not type == "send":
        return False

    if type == "send":
        node_url = transaction.origin.wallet.node.URL
        work = transaction.origin.POW
        wallet = transaction.origin.wallet.wallet_id
        account = transaction.origin.address
        link = transaction.destination.address
        amount = str(int(account_info['balance']) - int(transaction.amount))

    if type == "receive":
        node_url = transaction.destination.wallet.node.URL
        work = transaction.destination.POW
        wallet = transaction.destination.wallet.wallet_id
        account = transaction.destination.address

        link = None
        while not link:
            link = transaction.transaction_hash_sending
            transaction = get_transaction(transaction.id)
            time.sleep(.2)

        amount = str(int(account_info['balance']) + int(transaction.amount))

    headers = {
        'Content-Type': 'application/json',
    }

    data_create_block = {
        "action": "block_create",
        "type": "state",
        "previous": account_info['frontier'],
        "account": account,
        "representative": account_info['representative'],
        "balance": amount,
        "link": link,
        "wallet": wallet,
        "work": work,
        "id": str(transaction.id),
    }

    logger.info(data_create_block)
    sent_successful = False

    response = retry(lambda: requests.post(node_url, headers=headers, data=json.dumps(data_create_block)), retries=5)

    if response.status_code == requests.codes.ok:
        sent_successful = True

    create_block_response = json.loads(response.text)
    block_for_proccessing = {
        "action": "process",
        "block": create_block_response['block'],
        "watch_work": False
    }

    response = retry(lambda: requests.post(node_url, headers=headers, data=json.dumps(block_for_proccessing)), retries=5)
    response_json = json.loads(response.text)
    hash_value = response_json['hash']

    if type == "send":
        transaction.transaction_hash_sending = hash_value
        logger.info("Send hash %s", hash_value)

    if type == "receive":
        transaction.transaction_hash_receiving = hash_value
        logger.info("Receive hash %s", hash_value)

    retry(lambda: transaction.save())

    if response.status_code != requests.codes.ok:
        sent_successful = False

    return sent_successful, hash_value
