from ..nano_services.node_service import NodeService
from ..models.nano_models.node import Node
from ..models.nano_models.wallet import Wallet
from ..models.token_models.application import Application


class Bootstrap:

    def __init__(self, application_id):
        self.application = Application.objects.get(application_id=application_id)

    def bootstrap_application(self):
        self.bootstrap_ping_nodes()

    """
    Validates nodes are active and available
    """
    def bootstrap_ping_nodes(self):
        nodes = Node.objects.filter(application=self.application).all()
        for node in nodes:
            node_service = NodeService(node)
            node_available = node_service.ping_node()

            if not node_available:
                raise Exception("Node {0} not available".format(node.URL))

    """
    Create new wallets
    """
    def bootstrap_create_wallets(self):
        wallets = Wallet.objects.filter(application=self.application).all()
        for wallet in wallets:
            pass





