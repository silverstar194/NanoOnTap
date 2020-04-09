from django.test import TestCase

from token_api.models.device import Device

from token_api.token_services.template import import_template


class TestVaildPolicy(TestCase):
    def setUp(self):
        pass

    def test_load_devices(self):
        file = "backend/token_api/tests/test_templates/load_devices.json"
        template = open(file).read()
        import_template(template)

        assert(Device.objects.all().count() == 3)
        assert (Device.objects.filter(device_id="device_one").count() == 1)
        assert (Device.objects.filter(device_id="device_two").count() == 1)
        assert (Device.objects.filter(device_id="device_three").count() == 1)



