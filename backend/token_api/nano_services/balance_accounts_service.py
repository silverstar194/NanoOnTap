import nano
from ..common.retry import retry
from multiprocessing.pool import ThreadPool

from ..models.nano_models.account import Account

import logging
logger = logging.getLogger(__name__)


class BalanceAccount:

    def sync_accounts(self):
        thread_pool = ThreadPool(processes=4)
        all_accounts = Account.objects.all()
        for account in all_accounts:
            thread_pool.apply_async(self.check_account_balance_async, (account,))

        thread_pool.close()
        thread_pool.join()

    def check_account_balance_async(self, account):
        """
        Check for correct balance with node.
        :param account:
        :returns PoW valid on account
        """
        account.lock()
        logger.info('Syncing account balance: %s' % account)

        rpc = retry(lambda: nano.rpc.Client(account.wallet.node.URL))

        new_balance = retry(lambda: rpc.account_balance(account=account.address)['balance'])

        if not account.current_balance == new_balance:
            logger.error('Updating balance %s' % (account.address))
            account.current_balance = new_balance
            account.POW = None
        account.unlock()