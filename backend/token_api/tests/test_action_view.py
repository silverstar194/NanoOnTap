from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestActionView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_actions(self):
        client = Client()
        response = client.post(reverse('action/action/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert len(content) == 1

        # check model
        assert 'model' in content[0]
        assert content[0]['model'] == 'action'
        assert content[0]['fields']['action_name'] == "Send 1 Nano"

    def test_get_action(self):
        client = Client()
        response = client.post(reverse('action/action/get'), data=json.dumps({"application": "app_one", "action_name": "Send 1 Nano" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'action'
        assert content[0]['fields']['action_name'] == "Send 1 Nano"

    def test_update_action(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/action/update'), data=json.dumps({"model":"action","fields":{"action_name":"Send 1 Nano","from_account":["account_one"],"to_account":["account_two"],"amount":0,"application":["app_one"],"priority":100}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Action updated"

        response_changed = client.post(reverse('action/action/get'), data=json.dumps({"application": "app_one", "action_name": "Send 1 Nano"}), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'action'
        assert content_changed[0]['fields']['amount'] == 0

    def test_remove_action(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/action/remove'), data=json.dumps({"application": "app_one", "action_name": "Send 1 Nano" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






