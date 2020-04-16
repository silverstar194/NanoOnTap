import logging


import nano

from .. import models as models
from ..common.retry import retry

logger = logging.getLogger(__name__)


class AccountService:

    def __init__(self, account):
        self.account = account
        self.node = account.wallet.node
        self.rpc = nano.rpc.Client(self.node.URL)
        self.wallet = account.wallet

    def create_account_if_not_exists(self):
        if not self.ping_account():
            address = retry(lambda: self.rpc.account_create(wallet=self.account.wallet.wallet_id))
            self.account.address = address
            self.account.save()
            logger.info("Created account {0} address {1} in wallet {2}".format(self.account.account_id, self.account.address, self.wallet))
        else:
            logger.info("Account {0} address {1} already exists in wallet {2}".format(self.account.account_id, self.account.address, self.wallet))

    def ping_account(self):
        try:
            return (self.rpc.wallet_contains(self.account.wallet.wallet_id, self.account.address), self.account.address)
        except Exception:
            logger.info("Cannot ping account {0} address {1} in wallet {2}".format(self.account.account_id, self.account.address, self.wallet))
            return False

    @staticmethod
    def get_accounts():
        return retry(lambda: models.Account.objects.all())

    @staticmethod
    def number_accounts(self):
        return models.Account.objects.all().count()

    def clear_receive_accounts():
        """
        Fetches all receive block with the nano network across accounts.

        @raise RPCException: RPC Failure
        """
        accounts_list = get_accounts() # Not great all threads will vaildate TODO

        thread_pool = ThreadPool(processes=4)
        for account in accounts_list:
            thread_pool.apply_async(clear_frontier_async, (account,))
        thread_pool.close()
        thread_pool.join()


    def unlock_all_accounts():
        """
        Unlock all the account at once for speed at DB layer
        """
        retry(lambda: models.Account.objects.all().update(in_use=False))


    def lock_all_accounts():
        """
        Lock all the account at once for speed at DB layer
        """
        retry(lambda: models.Account.objects.all().update(in_use=True))
    #
    #
    # def clear_frontier_async(account):
    #     """
    #     Clears out any pending receive blocks node does not auto process.
    #     :param account:
    #     """
    #     logger.info('Clearing possible receive blocks from account %s' % account.address)
    #
    #     pending_blocks = None
    #     try:
    #         rpc = nano.rpc.Client(account.wallet.node.URL)
    #         address_nano = account.address.replace("xrb", "nano")
    #         pending_blocks = retry(lambda: rpc.accounts_pending([account.address])[address_nano])
    #     except Exception as e:
    #         logger.exception('RCP call failed during receive %s' % str(e.message))
    #
    #     for block in pending_blocks:
    #         logger.info("Found block %s to receive for %s " % (block, account.address))
    #
    #         if not validate_or_regenerate_PoW(account):
    #             logger.error('Total faliure of dPoW. Aborting receive account %s' % account.address)
    #             continue
    #
    #         if len(pending_blocks) > 1:
    #             time.sleep(1)  ## Allow frontier to refresh
    #
    #         try:
    #             received_block = retry(lambda: rpc.receive(wallet=account.wallet.wallet_id, account=account.address, work=account.POW, block=block))
    #             logger.info('Received block %s to %s' % (received_block, account.address))
    #         except nano.rpc.RPCException as e:
    #             logger.exception('Error during clean up receive account %s block %s ' % (account.address, block, str(e)))
    #
    #
    # def validate_or_regenerate_PoW(account):
    #     """
    #     Check for valid PoW and regenerates if needed.
    #     :param account:
    #     :returns PoW valid on account
    #     """
    #
    #     rpc = nano.rpc.Client(account.wallet.node.URL)
    #     valid_PoW = validate_PoW(account)
    #
    #     # Make sure the POW is there (not in the POW regen queue) if not wait for it and its valid
    #     count = 0
    #     while not valid_PoW and count < 3:
    #         try:
    #             account.POW = None
    #             retry(lambda: account.save())
    #             address_nano = account.address.replace("xrb", "nano")
    #             frontier = retry(lambda: rpc.frontiers(account=account.address, count=1)[address_nano])
    #             POWService.enqueue_account(address=account.address, frontier=frontier, urgent=True)
    #             logger.info('Generating PoW during validate_PoW for: %s' % account.address)
    #             count += 1
    #         except Exception as e:
    #             count += 1
    #             if count >= 3:
    #                 logger.error('Error adding address, frontier pair to POWService: %s' % e)
    #
    #         wait_on_PoW = 0
    #         while not valid_PoW and wait_on_PoW < 7:
    #             wait_on_PoW += 1
    #             account = get_account(account.address)
    #             valid_PoW = validate_PoW(account)
    #             time.sleep(1)
    #
    #     ##Still no dPoW....
    #     if not valid_PoW:
    #         logger.error('Total failure of dPoW. Aborting transaction account %s' % account.address)
    #         account.POW = None
    #         retry(lambda: account.save())
    #
    #     return valid_PoW


    @staticmethod
    def validate_PoW(account):
        """
        Check for valid PoW.
        :param account:
        :returns PoW valid on account
        """
        rpc = nano.rpc.Client(account.wallet.node.URL)
        frontier = retry(lambda: list(rpc.frontiers(account=account.address, count=1).values())[0])
        valid_PoW = False

        if not account.POW:
            logger.error('PoW None')
            return valid_PoW, frontier

        try:
            valid_PoW = retry(lambda: rpc.work_validate(work=account.POW, hash=frontier))
        except Exception as e:
            logger.exception('PoW invalid during validate_PoW %s' % str(e))

        if not valid_PoW:
            logger.error('PoW invalid work %s frontier %s' % (account.POW, frontier))

        return valid_PoW, frontier

    @staticmethod
    def ad_hoc_validation_or_regeneration(account):
        from .pow_service import POWService
        if not AccountService.validate_PoW(account):
            try:
                POWService.ad_hoc_pow(account)
            except Exception:
                return False

        return True
