from django.test import TestCase

from token_api.models.account import Account
from token_api.models.node import Node
from token_api.models.transaction import Transaction
from token_api.models.wallet import Wallet

from token_api.models.action import Action
from token_api.models.actionhistory import ActionHistory
from token_api.models.accountpolicy import AccountPolicy
from token_api.models.actionpolicy import ActionPolicy
from token_api.models.device import Device
from token_api.models.token import Token

from token_api.token_services.actionexecution import action_execution


class TestVaildPolicy(TestCase):
    def setUp(self):
        self.test_node = Node.objects.create(id=1,
                                        URL="http://127.0.0.1:7076",
                                        latitude=1.1,
                                        longitude=1.1,
                                        location_name="Testville, USA")

        self.test_wallet = Wallet.objects.create(node=self.test_node,
                                            wallet_id=1)

        self.token = Token.objects.create(token_id = "token_one")

        self.account_one = Account.objects.create(id=1,
                                                wallet=self.test_wallet,
                                                address=
                                                "xrb_3er5ka9cx6nxtcfapcj77za3n4ne74xbp9b6sbxnuzan9iorxj3xoyy6h1n1",
                                                current_balance=100,
                                                POW="POW")

        self.account_two = Account.objects.create(id=2,
                                                wallet=self.test_wallet,
                                                address=
                                                "xrb_3stk814q3ksqopqgeemzk7kduyjzhu355dmmon3ypco3dwbrm6c93wgspsy6",
                                                current_balance=0,
                                                POW="POW", token=self.token)

        self.test_device = Device.objects.create(device_id="device_one")

        self.test_action = Action.objects.create(from_account=self.account_one, to_account=self.account_two, amount=1, priority=200, device=self.test_device)
        self.action_policy = ActionPolicy.objects.create(priority = 200, token=self.token)

    def test_single_action_single_policy(self):
        print("\ntest_single_action_single_policy")
        action_execution("device_one", "token_one")
        assert (ActionHistory.objects.filter(action__device__device_id="device_one").count() == 1)
        assert (ActionHistory.objects.filter(action__device__device_id="device_one").count() == 1)

        ActionHistory.objects.get(action__device__device_id="device_one").delete()


    def test_no_action_on_device(self):
        print("\ntest_no_action_on_device")
        action = self.test_action
        temp = action.device
        action.device = None;
        action.save()

        action_execution("device_one", "token_one")

        assert (ActionHistory.objects.all().count() == 0)

        action.device = temp;
        action.save()

    def test_no_policy_on_token(self):
        print("\ntest_no_policy_on_token")
        policy = self.action_policy
        temp = policy.token
        policy.token = None;
        policy.save()

        self.assertRaises(Exception, action_execution, "device_one", "token_one")

        assert (ActionHistory.objects.count() == 0)

        assert (ActionHistory.objects.count() == 0)

        policy.token = temp
        policy.save()


    def test_high_action_priority(self):
        print("\ntest_high_action_priority")
        Action.objects.create(from_account=self.account_one, to_account=self.account_two, amount=1, priority=100, device = self.test_device)

        action_execution("device_one", "token_one")

        assert (ActionHistory.objects.filter(action__device__device_id="device_one").count() == 1)
        action_completed = ActionHistory.objects.filter(action__device__device_id="device_one").get()

        assert (action_completed.action.priority == 100)
        assert (action_completed.policy.priority == 200)

        action_completed.delete()





