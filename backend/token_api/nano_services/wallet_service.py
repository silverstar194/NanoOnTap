import nano

from ..common.retry import retry

import logging
logger = logging.getLogger(__name__)


class WalletService:

    def __init__(self, wallet):
        self.wallet = wallet
        self.node = wallet.node
        self.rpc = nano.rpc.Client(self.node.URL)

    def create_wallet_if_not_exists(self):
        """
        Create a new wallet from the given information if it does not already exist
        """
        if not self.ping_wallet():
            wallet_id = retry(lambda: self.rpc.wallet_create())
            self.wallet.wallet_id = wallet_id
            self.wallet.save()
            logger.info("Created wallet {0} on node {1}".format(self.wallet, self.node))
        else:
            logger.info("Wallet {0} already exists on node {1}".format(self.wallet, self.node))

    def ping_wallet(self):
        """
            Validate wallet exists on node
        """
        if self.wallet.wallet_id:
            try:
                retry(lambda: self.rpc.account_list(wallet=self.wallet.wallet_id))
            except Exception:
                return False
            return True
        return False

