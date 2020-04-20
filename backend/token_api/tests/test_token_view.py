from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestTokenView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_tokens(self):
        client = Client()
        response = client.post(reverse('action/token/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        assert len(content) == 1

        # check model
        assert 'model' in content[0]
        assert content[0]['model'] == 'token'
        assert content[0]['fields']['token_name'] == "token_one"

    def test_get_token(self):
        client = Client()
        response = client.post(reverse('action/token/get'), data=json.dumps({"application": "app_one", "token_name": "token_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'token'
        assert content[0]['fields']['token_name'] == "token_one"

    def test_update_token(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/token/update'), data=json.dumps({"model":"token","fields":{"token_name":"token_one","application":["app_one"],"action_polices":[["Allow All"]],"custom_action_polices":[]}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Token updated"

        response_changed = client.post(reverse('action/token/get'), data=json.dumps({"application": "app_one", "token_name": "token_one" }), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'token'

        assert content_changed[0]['fields']['application'] == ["app_one"]

    def test_remove_token(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/token/remove'), data=json.dumps({"application": "app_one", "token_name": "token_one" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






