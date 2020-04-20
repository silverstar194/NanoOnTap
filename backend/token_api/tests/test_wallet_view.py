from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestWalletView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_wallets(self):
        client = Client()
        response = client.post(reverse('action/wallet/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert len(content) == 1

        # check model
        assert 'model' in content[0]
        assert content[0]['model'] == 'wallet'
        assert content[0]['fields']['wallet_name'] == 'wallet_one'

    def test_get_wallet_not_exists(self):
        client = Client()
        response = client.post(reverse('action/wallet/get'), data=json.dumps({"application": "app_one", "wallet_one": "NONE" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert content == []

    def test_get_wallet(self):
        client = Client()
        response = client.post(reverse('action/wallet/get'), data=json.dumps({"application": "app_one", "wallet_name": "wallet_one" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'wallet'
        assert content[0]['fields']['wallet_name'] == 'wallet_one'
        assert content[0]['fields']['node'][0] == 'node_one'

    def test_update_wallet(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/wallet/update'), data=json.dumps({"model":"wallet","fields":{"node":["node_one"],"wallet_name":"wallet_changed","application":["app_one"]}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Wallet updated"

        response_changed = client.post(reverse('action/wallet/get'), data=json.dumps({"application": "app_one", "wallet_name": "wallet_changed"}), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'wallet'
        assert content_changed[0]['fields']['wallet_name'] == 'wallet_changed'

    def test_remove_wallet(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/wallet/remove'), data=json.dumps({"application": "app_one", "wallet_name": "wallet_one" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






