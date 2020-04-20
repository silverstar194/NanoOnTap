from django.test import TestCase

from token_api.token_services.template_deserializer import import_template

from token_api.token_services.template_serializer import export_template

import json

class TestExportImportTemplate(TestCase):

    def test_import_file(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

    def test_export_file(self):
        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)

        export_template("app_one")

    def test_import_export(self):

        with open('backend/token_api/tests/templates/template_one.json') as json_file:
            data = json_file.read()
            import_template(data)
            imported_data = json.loads(data)

        exported_data = export_template("app_one")
        assert exported_data == imported_data
