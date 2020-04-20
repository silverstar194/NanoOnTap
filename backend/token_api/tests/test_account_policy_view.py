from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestAccountPolicyView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_account_policies(self):
        client = Client()
        response = client.post(reverse('action/accountpolicy/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        assert len(content) == 1

        # check model
        assert 'model' in content[0]
        assert content[0]['model'] == 'accountpolicy'
        assert content[0]['fields']['policy_name'] == "Allow All"

    def test_get_account_policy(self):
        client = Client()
        response = client.post(reverse('action/accountpolicy/get'), data=json.dumps({"application": "app_one", "policy_name": "Allow All" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'accountpolicy'
        assert content[0]['fields']['policy_name'] == "Allow All"

    def test_update_account_policy(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/accountpolicy/update'), data=json.dumps({"model":"accountpolicy","fields":{"policy_name":"Allow All","application":["app_one"],"send_action_limit":0,"receive_action_limit":-1,"send_amount_limit":-1,"receive_amount_limit":-1}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Account Policy updated"

        response_changed = client.post(reverse('action/accountpolicy/get'), data=json.dumps({"application": "app_one", "policy_name": "Allow All"}), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'accountpolicy'
        assert content_changed[0]['fields']['send_action_limit'] == 0

    def test_remove_account_policy(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/accountpolicy/remove'), data=json.dumps({"application": "app_one", "policy_name": "Allow All" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






