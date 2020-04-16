from ..nano_services.node_service import NodeService
from ..nano_services.wallet_service import WalletService
from ..models.nano_models.node import Node
from ..models.nano_models.wallet import Wallet
from ..models.token_models.application import Application
from ..models.nano_models.account import Account
from ..nano_services.account_service import AccountService

import logging
logger = logging.getLogger(__name__)


class Bootstrap:

    def __init__(self, application_id):
        self.application = Application.objects.get(application_id=application_id)

    def bootstrap_application(self):
        logger.info("=== Starting bootstrap ===")

        self.bootstrap_ping_nodes()
        self.bootstrap_create_wallets()
        self.bootstrap_create_accounts()

        logger.info("=== Completed bootstrap ===")

    """
    Validate nodes are active and available
    """
    def bootstrap_ping_nodes(self):
        nodes = Node.objects.filter(application=self.application).all()
        for node in nodes:
            node_service = NodeService(node)
            node_available = node_service.ping_node()

            if not node_available:
                raise Exception("Node {0} not available".format(node.URL))

    """
    Create new wallets if they have not been created already
    """
    def bootstrap_create_wallets(self):
        wallets = Wallet.objects.filter(application=self.application).all()
        for wallet in wallets:
            wallet_service = WalletService(wallet)
            wallet_service.create_wallet_if_not_exists()

    """
    Create new accounts if they have not been created already
    """
    def bootstrap_create_accounts(self):
        accounts = Account.objects.filter(application=self.application).all()
        for account in accounts:
            account_service = AccountService(account)
            account_service.create_account_if_not_exists()



