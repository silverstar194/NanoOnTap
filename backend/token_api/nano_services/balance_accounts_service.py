from django.db.utils import OperationalError


import nano
from ..common.retry import retry
import logging


from ..models.nano_models.account import Account


logger = logging.getLogger(__name__)


class BalanceAccount:

    @staticmethod
    def sync_accounts():
        all_accounts = Account.objects.all()

        try:
            for account in all_accounts:
                BalanceAccount.check_account_balance(account)
        except OperationalError:
            pass

    @staticmethod
    def check_account_balance(account):
        logger.info('Syncing account balance: %s' % account)
        account = Account.objects.get(address=account.address)

        rpc = retry(lambda: nano.rpc.Client(account.wallet.node.URL))

        new_balance = retry(lambda: rpc.account_balance(account=account.address)['balance'])

        if not account.current_balance == new_balance:
            account.current_balance = new_balance
            account.POW = None
        account.save()
