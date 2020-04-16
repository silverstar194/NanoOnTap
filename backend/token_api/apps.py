from django.apps import AppConfig

import logging
logger = logging.getLogger(__name__)

class TokenApiConfig(AppConfig):
    name = 'token_api'

    def ready(self):
        from .nano_services.pow_service import POWService
        from .nano_services.balance_accounts_service import BalanceAccount

        logger.info('Starting POWService and running POW_accounts()...')
        POWService.start()
        POWService.POW_accounts()

        logger.info('Starting sync accounts')
        BalanceAccount().sync_accounts()
