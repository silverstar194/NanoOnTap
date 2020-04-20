
from django.test import TestCase

from token_api.token_services.template_deserializer import import_template

from token_api.token_services.executor import Executor

from token_api.models.token_models.device import Device

from token_api.models.token_models.token import Token

from token_api.models.token_models.application import Application

class TestSimple(TestCase):
    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_simple_send(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set.action_set_name == "Pay Single Account"
        assert valid_policy.policy_name == "Allow All"


    def test_remove_allowed_device(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Remove allowed device_one
        allowed_device = token.action_polices.get(policy_name="Allow All").allowed_devices.get(device_name="device_one")
        allowed_device.delete()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None


    def test_add_denied_device(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Add device_one to denied device list
        denied_devices = token.action_polices.get(policy_name="Allow All").denied_devices
        denied_devices.add(device)

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_remove_allowed_to_account(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Remove allowed to_account (aka all accounts are now allowed)
        to_accounts = token.action_polices.get(policy_name="Allow All").allowed_to_accounts
        to_account = token.action_polices.get(policy_name="Allow All").allowed_to_accounts.get(account_name="account_two")
        to_accounts.remove(to_account)

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_add_denied_to_account(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Remove allowed to_account (aka all accounts are not allowed)
        denied_to_accounts = token.action_polices.get(policy_name="Allow All").denied_to_accounts
        to_account = token.action_polices.get(policy_name="Allow All").allowed_to_accounts.get(account_name="account_two")
        denied_to_accounts.add(to_account)

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_remove_allowed_from_account(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Remove allowed from_account (aka all accounts are now allowed)
        allowed_from_accounts = token.action_polices.get(policy_name="Allow All").allowed_from_accounts
        from_account = token.action_polices.get(policy_name="Allow All").allowed_from_accounts.get(account_name="account_one")
        allowed_from_accounts.remove(from_account)

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_add_denied_from_account(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        # Remove allowed to_account (aka all accounts are not allowed)
        denied_from_accounts = token.action_polices.get(policy_name="Allow All").denied_from_accounts
        from_account = token.action_polices.get(policy_name="Allow All").allowed_from_accounts.get(account_name="account_one")
        denied_from_accounts.add(from_account)

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_action_set_action_limit(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        action_policy = token.action_polices.get(policy_name="Allow All")
        action_policy.action_limit = 0
        action_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_action_set_send_limit(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        action_policy = token.action_polices.get(policy_name="Allow All")
        action_policy.action_limit = 0
        action_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_account_send_amount(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        from_account = token.action_polices.get(policy_name="Allow All").allowed_from_accounts.get(account_name="account_one")
        from_account_policy = from_account.account_policies.first()

        from_account_policy.send_amount_limit = 0
        from_account_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_account_send_limit(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        from_account = token.action_polices.get(policy_name="Allow All").allowed_from_accounts.get(account_name="account_one")
        from_account_policy = from_account.account_policies.first()
        from_account_policy.send_action_limit = 0
        from_account_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_account_receive_amount(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        to_account = token.action_polices.get(policy_name="Allow All").allowed_to_accounts.get(account_name="account_two")
        to_account_policy = to_account.account_policies.first()
        to_account_policy.receive_amount_limit = 0
        to_account_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None

    def test_account_receive_limit(self):
        device = Device.objects.get(application__application_name="app_one")
        token = Token.objects.get(application__application_name="app_one")
        application = Application.objects.get(application_name="app_one")

        assert device.device_name == "device_one"
        assert token.token_name == "token_one"

        to_account = token.action_polices.get(policy_name="Allow All").allowed_to_accounts.get(account_name="account_two")
        to_account_policy = to_account.account_policies.first()
        to_account_policy.receive_action_limit = 0
        to_account_policy.save()

        executor = Executor(device, token, application, debug=True)
        action_set, valid_policy = executor.run_action_set()

        assert action_set == None
        assert valid_policy == None
