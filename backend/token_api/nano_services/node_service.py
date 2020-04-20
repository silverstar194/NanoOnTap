from ..common.retry import retry
import nano
import logging


logger = logging.getLogger(__name__)


class NodeService:
    def __init__(self, node):
        self.node = node

    def ping_node(self):
        try:
            retry(lambda: nano.rpc.Client(self.node.URL).version())
            logger.info("Pinged node {0}".format(self.node))
        except Exception as e:
            logger.error("Error pinging node {0}".format(e))
            return False
        return True
