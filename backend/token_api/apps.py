from django.apps import AppConfig

import logging

logger = logging.getLogger(__name__)


class TokenApiConfig(AppConfig):
    name = 'token_api'

    def ready(self):
<<<<<<< HEAD
        from .nano_services.pow_service import POWService
        from .nano_services.balance_accounts_service import BalanceAccount
        from .nano_services.account_service import AccountService

        logger.info('Starting POWService and running POW_accounts()...')
        POWService.start()
        POWService.POW_accounts()

        logger.info('Starting sync accounts')
        BalanceAccount().sync_accounts()
        AccountService.clear_receive_accounts()
=======
        try:
            from .nano_services.pow_service import POWService
            from .nano_services.balance_accounts_service import BalanceAccount
            from .nano_services.account_service import AccountService

            logger.info('Starting POWService and running POW_accounts()...')
            POWService.start()
            POWService.POW_accounts()

            logger.info('Starting sync accounts')
            BalanceAccount().sync_accounts()
            AccountService.clear_receive_accounts()
        except Exception:
            logger.error("Could not run start up script...")
>>>>>>> 34299db7758d56f978ce8f136224cc73831fc2e0
