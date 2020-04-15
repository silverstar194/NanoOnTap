import nano

from ..common.retry import retry

class WalletService:

    def __init__(self, wallet):
        self.wallet = wallet

    def create_wallet_if_not_exists(node):
        """
        Create a new wallet from the given information

        @param node: Node the wallet lives on
        @param wallet_id: The seed of the wallet, if None generate a new wallet on the node
        @return: New wallet object
        """
        rpc = nano.rpc.Client(node.URL)
        wallet_id = retry(lambda: rpc.wallet_create())
        return wallet_id


    def ping_wallet(self, node):
        """
        Get all wallets in the database

        @enabled: Filter based on wallet's node enability
        @return: Query of all wallets
        """
        rpc = nano.rpc.Client(node.URL)

        return retry(lambda: rpc.account_list(wallet=self.wallet.wallet_id))
