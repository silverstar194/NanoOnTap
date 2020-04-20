from django.test import TestCase

from token_api.token_services.template_deserializer import import_template

from django.test import Client
from django.urls import reverse

import json


class TestAccountView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_accounts(self):
        client = Client()
        response = client.post(reverse('action/account/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert len(content) == 2

        # check models
        assert 'model' in content[0]
        assert content[0]['model'] == 'account'
        assert content[0]['fields']['account_name'] == 'account_one'

        assert 'model' in content[1]
        assert content[1]['model'] == 'account'
        assert content[1]['fields']['account_name'] == 'account_two'

    def test_get_account_not_exists(self):
        client = Client()
        response = client.post(reverse('action/account/get'), data=json.dumps({"application": "app_one", "account_name": "NONE" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert content == []

    def test_get_account(self):
        client = Client()
        response = client.post(reverse('action/account/get'), data=json.dumps({"application": "app_one", "account_name": "account_one" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'account'
        assert content[0]['fields']['account_name'] == 'account_one'
        assert content[0]['fields']['wallet'][0] == 'wallet_one'

    def test_update_account(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/account/update'), data=json.dumps({'model': 'account', 'fields': {'account_name': 'account_changed', 'wallet': ['wallet_one'], 'application': ['app_one'], 'account_policies': [['Allow All']]}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Account updated"

        response_changed = client.post(reverse('action/account/get'), data=json.dumps({"application": "app_one", "account_name": "account_changed"}), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'account'
        assert content_changed[0]['fields']['account_name'] == 'account_changed'
        assert content_changed[0]['fields']['wallet'][0] == 'wallet_one'


    def test_remove_account(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/account/remove'), data=json.dumps({"application": "app_one", "account_name": "account_one" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






