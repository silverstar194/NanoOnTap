from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestTransactionView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_action_history(self):
        client = Client()
        response = client.post(reverse('action/actionhistory/get'), data=json.dumps({"application": "app_one", "action_name":"Send 1 Nano"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        assert response.status_code == 200
