from django.test import TestCase


from token_api.token_services.bootstrap import Bootstrap
from token_api.token_services.template_deserializer import import_template
from token_api.models.token_models.application import Application


class TestBootstrap(TestCase):

    def test_boostrap_node(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        application = Application.objects.get(application_name="app_one")
        bootstrapper = Bootstrap(application)
        bootstrapper.bootstrap_ping_nodes()