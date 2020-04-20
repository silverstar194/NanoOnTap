from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestNodeView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_nodes(self):
        client = Client()
        response = client.post(reverse('action/node/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check models
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'node'
        assert content[0]['fields']['node_name'] == 'node_one'

    def test_get_node_not_exists(self):
        client = Client()
        response = client.post(reverse('action/node/get'), data=json.dumps({"application": "app_one", "node_name": "NONE" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']
        assert content == []

    def test_get_node(self):
        client = Client()
        response = client.post(reverse('action/node/get'), data=json.dumps({"application": "app_one", "node_name": "node_one" }), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'node'
        assert content[0]['fields']['node_name'] == 'node_one'
        assert content[0]['fields']['URL'] == 'https://frankfurt.rcp.nanospeed.live/'

    def test_update_node(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/node/update'), data=json.dumps({"model":"node", "fields": {"URL":"https://frankfurt.rcp.nanospeed.live/", "node_name":"node_changed", "application": ["app_one"]}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Node updated"

        response_changed = client.post(reverse('action/node/get'), data=json.dumps({"application": "app_one", "node_name": "node_changed"}), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'node'
        assert content_changed[0]['fields']['node_name'] == 'node_changed'
        assert content_changed[0]['fields']['URL'] == 'https://frankfurt.rcp.nanospeed.live/'

    def test_remove_node(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/node/remove'), data=json.dumps({"application": "app_one", "node_name": "node_one" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






