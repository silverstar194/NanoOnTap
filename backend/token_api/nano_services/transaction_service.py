import requests
import nano


from .account_service import AccountService
from .pow_service import POWService
from ..common.retry import *
from ..models.token_models.transaction import Transaction


logger = logging.getLogger(__name__)


class AccountBalanceMismatchException(Exception):
    def __init__(self, balance_actual, balance_db, account):
        Exception.__init__(self, "{0} != {1} for account: {2}".format(balance_actual, balance_db, account))


class InsufficientNanoException(Exception):
    def __init__(self):
        Exception.__init__(self, "The Nano account did not have enough RAW to make a transaction.")


class NegativeNanoException(Exception):
    def __init__(self):
        Exception.__init__(self, "The send amount must be positive")


class AddressDoesNotExistException(Exception):
    def __init__(self, account, wallet):
        Exception.__init__(self, "The Nano address {0} does not exist on wallet {1}".format(account, wallet))


class NoIncomingBlocksExceFDeption(Exception):
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

class RCPException(Exception):
    def __init__(self):
        Exception.__init__(self, "Failed to communicate with nodes")

class TransactionService:

    def __init__(self):
        self.pow_service = POWService()

    def new_transaction(self, application, origin_account, destination_account, amount):
        if amount < 0:
            logger.exception("Cannot send negative amount %s." % amount)
            raise NegativeNanoException()

        transaction = Transaction(
            origin=origin_account,
            destination=destination_account,
            amount=amount,
            application=application
        )

        transaction.save()

        return transaction

    def send_transaction(self, transaction):

        rpc_origin_node = nano.rpc.Client(transaction.origin.wallet.node.URL)
        rpc_destination_node = nano.rpc.Client(transaction.destination.wallet.node.URL)

        if (transaction.origin.current_balance - transaction.amount < 0):
            logger.info("InsufficientNanoException %s" % transaction.origin.address)
            raise InsufficientNanoException()

        if not AccountService.ad_hoc_validation_or_regeneration(transaction.origin):
            logger.error('Total faliure of dPoW. Aborting transaction account %s' % transaction.origin.address)
            raise InvalidPOWException()

        transaction.origin = AccountService.get_account(transaction.origin.address)

        try:
            logger.info("Transaction for send block status before_send")
            account_info = retry(lambda: rpc_origin_node.account_info(transaction.origin.address, representative=True))

            sent_done, hash_value = self.create_and_process(transaction, transaction.origin.current_balance, account_info, "send")

            if not sent_done:
                logger.error("Error in create and process send")
                raise RCPException()

            logger.info("Transaction in status send to node %s " % transaction.transaction_hash_sending)

            # Update the balances and POW
            transaction.origin.current_balance = transaction.origin.current_balance - transaction.amount
            transaction.destination.current_balance = transaction.destination.current_balance + transaction.amount
            transaction.origin.POW = None

        except nano.rpc.RPCException as e:
            logger.exception("RPCException one %s" % e)
            raise RCPException()

        retry(lambda: transaction.origin.save())
        retry(lambda: transaction.destination.save())
        retry(lambda: transaction.save())

        # Regenerate PoW
        POWService.enqueue_account(account=transaction.origin, frontier=transaction.transaction_hash_sending)

        # Return as soon as transaction_hash_receiving is available
        transaction = self.send_receive_block(transaction, rpc_destination_node)

        return transaction

    def send_receive_block(self, transaction, rpc_destination_node):

        if not AccountService.ad_hoc_validation_or_regeneration(transaction.destination):
            logger.error('Total failure of dPoW. Aborting transaction account %s' % transaction.destination.address)
            raise InvalidPOWException()

        transaction.destination = AccountService.get_account(transaction.destination.address)

        try:
            logger.info("Transaction for receive block status before_receive")
            account_info = retry(lambda: rpc_destination_node.account_info(transaction.destination.address, representative=True))

            ##Create and process block work around
            receive_done, hash_value = self.create_and_process(transaction, transaction.destination.current_balance, account_info, "receive")
            if not receive_done:
                logger.exception("Error in create and process receive")
                raise RCPException()

        except nano.rpc.RPCException as e:
            logger.exception("RPCException two %s" % e)

            transaction.destination.POW = None
            frontier = retry(lambda: rpc_destination_node.frontiers(account=transaction.destination.address, count=1)[transaction.destination.address])
            POWService.enqueue_account(account=transaction.destination, frontier=frontier)

            raise RCPException()

        transaction.transaction_hash_receiving = hash_value

        retry(lambda: transaction.destination.save())
        retry(lambda: transaction.save())
        POWService.enqueue_account(account=transaction.destination, frontier=transaction.transaction_hash_receiving)

        return transaction

    def get_transaction(self, id):
        try:
            return retry(lambda: Transaction.objects.get(id=id))
        except Transaction.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned()

    def create_and_process(self, transaction, account_balance, account_info, type):

        if not type == "receive" and not type == "send":
            logger.error("block type not receive or send")
            return False

        if type == "send":
            node_url = transaction.origin.wallet.node.URL
            work = transaction.origin.POW
            wallet = transaction.origin.wallet.wallet_id
            account = transaction.origin.address
            link = transaction.destination.address
            amount = int(account_balance - transaction.amount)

        if type == "receive":
            node_url = transaction.destination.wallet.node.URL
            work = transaction.destination.POW
            wallet = transaction.destination.wallet.wallet_id
            account = transaction.destination.address

            link = None
            while not link:
                link = transaction.transaction_hash_sending
                transaction = self.get_transaction(transaction.id)
                time.sleep(.1)
            amount = account_balance

        headers = {
            'Content-Type': 'application/json',
        }

        data_create_block = {
            "action": "block_create",
            "type": "state",
            "previous": account_info['frontier'],
            "account": account,
            "representative": account_info['representative'],
            "balance": int(amount),
            "link": link,
            "wallet": wallet,
            "work": work,
            "id": str(transaction.id),
        }

        logger.info("Type {0} Block {1}".format(type, json.dumps(data_create_block)))
        sent_successful = False

        response = retry_post(lambda: requests.post(node_url, headers=headers, data=json.dumps(data_create_block)), item="block")

        if response.status_code == requests.codes.ok:
            sent_successful = True
        else:
            logger.info("Block failed to be created {}".format(response.text))

        create_block_response = json.loads(response.text)

        block_for_proccessing = {
            "action": "process",
            "block": create_block_response['block'],
        }

        response = retry_post(lambda: requests.post(node_url, headers=headers, data=json.dumps(block_for_proccessing)), item="hash")

        if response.status_code != requests.codes.ok:
            sent_successful = False
            logger.info("Block failed to be processed {0}".format(response.text))

        response_json = json.loads(response.text)
        if 'hash' not in response_json:
            logger.error("Create and process error {0}".format(response_json))

        hash_value = response_json['hash']

        if type == "send":
            transaction.transaction_hash_sending = hash_value
            logger.info("Send hash %s", hash_value)

        if type == "receive":
            transaction.transaction_hash_receiving = hash_value
            logger.info("Receive hash %s", hash_value)

        retry(lambda: transaction.save())

        return sent_successful, hash_value
