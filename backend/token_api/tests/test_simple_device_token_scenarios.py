
from django.test import TestCase

from token_api.token_services.template import import_template, export_template

from token_api.token_services.executor import run_action_set

from token_api.token_models.device import Device

class TestExportImportTemplate(TestCase):
    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_simple_send(self):
        device = Device.objects.get(application__application_id="app_one").first();
        token = ActionSet.objects.get(application__application_id="app_one").first();

        assert action_set.action_set_name === "Pay Single Account"
        run_action_set(action_set, )
