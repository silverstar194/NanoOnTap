
from django.test import TestCase

from token_api.token_services.template import import_template, export_template

from token_api.token_services.executor import Executor

from token_api.models.token_models.device import Device

from token_api.models.token_models.token import Token

from token_api.models.token_models.action_set import ActionSet

from token_api.models.token_models.application import Application


class TestExportImportTemplate(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_action_set_high_priority(self):
        device = Device.objects.get(application__application_id="app_one")
        token = Token.objects.get(application__application_id="app_one")
        application = Application.objects.get(application_id="app_one")

        assert device.device_id == "device_one"
        assert token.token_id == "token_one"

        action = device.action_sets.first().actions

        action_set_hi_pri = ActionSet.objects.create(action_set_name="High Pri", priority=0, application=application, actions=action)

        device.action_sets.add(action_set_hi_pri)

        executor = Executor(device, token)
        action_set, valid_policy = executor.run_action_set()

        assert action_set.action_set_name == action_set_hi_pri.action_set_name
        assert valid_policy.policy_name == "Allow All"


    def test_action_set_low_priority(self):
        device = Device.objects.get(application__application_id="app_one")
        token = Token.objects.get(application__application_id="app_one")
        application = Application.objects.get(application_id="app_one")

        assert device.device_id == "device_one"
        assert token.token_id == "token_one"

        action = device.action_sets.first().actions

        action_set_hi_pri = ActionSet.objects.create(action_set_name="High Pri", priority=1000, application=application, actions=action)

        device.action_sets.add(action_set_hi_pri)

        executor = Executor(device, token)
        action_set, valid_policy = executor.run_action_set()

        assert action_set.action_set_name == "Pay Single Account"
        assert valid_policy.policy_name == "Allow All"