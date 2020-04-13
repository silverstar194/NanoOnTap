
from django.test import TestCase

from token_api.token_services.template import import_template, export_template

from token_api.token_services.executor import Executor

from token_api.models.token_models.device import Device

from token_api.models.token_models.token import Token

class TestExportImportTemplate(TestCase):
    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_simple_send(self):
        device = Device.objects.get(application__application_id="app_one")
        token = Token.objects.get(application__application_id="app_one")

        assert device.device_id == "device_one"
        assert token.token_id == "token_one"

        executor = Executor(device, token)
        action_set, valid_policy = executor.run_action_set()

        assert action_set.action_set_name == "Pay Single Account"
        assert valid_policy.policy_name == "Allow All"