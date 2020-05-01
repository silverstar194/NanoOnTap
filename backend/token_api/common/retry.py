import time
import json

import logging

logger = logging.getLogger(__name__)

def retry(func, retries=8, pause=.09):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            logger.exception(e)
            if i < retries - 1: # i is zero indexed
                time.sleep(pause)
                pause = pause*1.5
                continue

            raise

"""
This adds a retry if block is rejected due to gateway timeout or accounts fail out of sync with node
"""
def retry_post(func, retries=8, pause=.09, item=None):
    from ..nano_services.pow_service import POWService
    from ..nano_services.balance_accounts_service import BalanceAccount
    from ..nano_services.account_service import AccountService
    for i in range(retries):
        try:
            res = func()
            res_json = json.loads(res.text)
            if item:
                res_json[item]
            return res
        except Exception as e:
            logger.exception(res.text)

            # resync is costly
            if "error" in res.text and i == 5: ## re sync accounts to recover after 5 tries
                logger.info('Recovering accounts (may take time)...')
                POWService.start()
                POWService.POW_accounts()
                BalanceAccount().sync_accounts()
                AccountService.clear_receive_accounts()
                continue

            logger.exception(e)
            if i < retries - 1: # i is zero indexed
                time.sleep(pause)
                pause = pause * 1.5
                continue

            raise
