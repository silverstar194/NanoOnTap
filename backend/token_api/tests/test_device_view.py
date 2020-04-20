from django.test import TestCase
from django.test import Client
from django.urls import reverse


import json


from token_api.token_services.template_deserializer import import_template


class TestDeviceView(TestCase):

    """
    Test valid setup between account_one and account_two. One device, one token, sending allowed.
    """
    def setUp(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_get_devices(self):
        client = Client()
        response = client.post(reverse('action/device/get/all'), data=json.dumps({"application": "app_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        assert len(content) == 1

        # check model
        assert 'model' in content[0]
        assert content[0]['model'] == 'device'
        assert content[0]['fields']['device_name'] == "device_one"

    def test_get_device(self):
        client = Client()
        response = client.post(reverse('action/device/get'), data=json.dumps({"application": "app_one", "device_name": "device_one"}), content_type='application/json')
        content = json.loads(response.content)

        # check message
        assert 'message' in content
        content = content['message']

        # check model
        assert len(content) == 1
        assert 'model' in content[0]
        assert content[0]['model'] == 'device'
        assert content[0]['fields']['device_name'] == "device_one"

    def test_update_device(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/device/update'), data=json.dumps({"model":"device", "fields":{"device_name":"device_one","application": ["app_one"] ,"action_sets": [["Pay Single Account"]]}}), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content
        assert content['message'] == "Device updated"

        response_changed = client.post(reverse('action/device/get'), data=json.dumps({"application": "app_one", "device_name": "device_one" }), content_type='application/json')
        content_changed = json.loads(response_changed.content)

        assert 'message' in content_changed
        content_changed = content_changed['message']

        assert len(content_changed) == 1
        assert 'model' in content_changed[0]
        assert content_changed[0]['model'] == 'device'

        assert content_changed[0]['fields']['application'] == ["app_one"]

    def test_remove_device(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        client = Client()
        response = client.post(reverse('action/device/remove'), data=json.dumps({"application": "app_one", "device_name": "device_one" }), content_type='application/json')
        content = json.loads(response.content)

        assert 'message' in content






