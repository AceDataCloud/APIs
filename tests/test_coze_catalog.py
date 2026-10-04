import importlib.util
import json
import unittest
from pathlib import Path

from openapi_spec_validator import validate_spec
from jsonschema import Draft4Validator

ROOT = Path(__file__).resolve().parents[1] / 'coze'
spec = importlib.util.spec_from_file_location('coze_build', ROOT / 'build_catalog.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class CozeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT / 'catalog/public-snapshot.json').read_text())
        cls.coverage = json.loads((ROOT / 'catalog/coverage.json').read_text())['services']
        cls.plugins = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'plugins').glob('*.json')}

    def test_every_public_service_is_accounted_for(self):
        self.assertEqual({x['id'] for x in self.source['services']}, {x['service_id'] for x in self.coverage})
        self.assertEqual(len(self.coverage), len({x['service_id'] for x in self.coverage}))
        for row in self.coverage:
            self.assertTrue(row['name'])
            self.assertTrue((ROOT / row['icon']).is_file())
            if row['service_type'] == 'Api':
                self.assertTrue(row['schema'] or row['blockers'])
            else:
                self.assertEqual('catalog_assistant', row['delivery'])

    def test_specs_are_valid_and_credentials_are_caller_owned(self):
        for key, definition in self.plugins.items():
            with self.subTest(service=key):
                validate_spec(definition)
                self.assertEqual('https://api.acedata.cloud', definition['servers'][0]['url'])
                operation_ids = []
                for path, methods in definition['paths'].items():
                    self.assertNotIn('/internal/', path)
                    for method, operation in methods.items():
                        self.assertNotEqual('delete', method)
                        operation_ids.append(operation['operationId'])
                        self.assertNotIn('__', operation['operationId'])
                        self.assertLessEqual(len(operation['operationId']), 64)
                        auth = [x for x in operation['parameters'] if x['name'] == 'Authorization']
                        self.assertEqual(1, len(auth))
                        self.assertTrue(auth[0]['required'])
                        self.assertNotIn('default', auth[0]['schema'])
                        self.assertNotIn('example', auth[0]['schema'])
                        body = operation.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                        if 'stream' in body.get('properties', {}):
                            self.assertEqual([False], body['properties']['stream']['enum'])
                self.assertEqual(len(operation_ids), len(set(operation_ids)))

    def test_compatibility_imports_preserve_routes_auth_and_file_parity(self):
        import yaml
        for key in ('claude', 'openai', 'kling', 'serp'):
            doc = json.loads((ROOT / 'imports' / f'{key}.json').read_text())
            self.assertEqual(doc, yaml.safe_load((ROOT / 'imports' / f'{key}.yaml').read_text()))
            validate_spec(doc)
            self.assertEqual(set(self.plugins[key]['paths']), set(doc['paths']))
            for path, methods in doc['paths'].items():
                for method, op in methods.items():
                    canonical = self.plugins[key]['paths'][path][method]
                    self.assertEqual(canonical['operationId'], op['operationId'])
                    self.assertEqual(canonical['parameters'], op['parameters'])
                    body = op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                    original = canonical.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                    self.assertTrue(set(original.get('required', [])) <= set(body.get('required', [])))
                    self.assertTrue(set(body.get('required', [])) <= set(body.get('properties', {})))

    def test_union_adapter_keeps_base_fields_and_required_inputs(self):
        # A conditional oneOf must not overwrite the request's normal fields.
        schema = {'type':'object','required':['query'],'properties':{'query':{'type':'string'},'count':{'type':'integer'}},'oneOf':[{'properties':{'mode':{'type':'string','enum':['a']}}},{'properties':{'mode':{'type':'string','enum':['b']}}}]}
        result = builder.import_body(schema)
        self.assertEqual({'query','count','mode'}, set(result['properties']))
        self.assertEqual(['query'], result['required'])
        self.assertEqual(2, len(result['oneOf']))
        for row in self.coverage:
            for item in row['operations']:
                if item['disposition'] != 'schema_prepared':
                    continue
                contract = self.source['contracts'][item['api_id']]['definition']
                original = contract['paths'][item['path']][item['method'].lower()]
                schema = original.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                schema = builder.resolve(schema, contract)
                built = self.plugins[row['key']]['paths'][item['path']][item['method'].lower()]
                body = built.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                self.assertTrue(set(schema.get('properties', {})) <= set(body.get('properties', {})), item['path'])
                self.assertTrue(set(schema.get('required', [])) <= set(body.get('required', [])), item['path'])

    def test_error_union_accepts_a_real_error_shape(self):
        operation=self.plugins['shorturl']['paths']['/shorturl']['post']
        schema=operation['responses']['401']['content']['application/json']['schema']
        Draft4Validator(schema).validate({'error':{'code':'invalid_token','message':'Invalid credential.'},'trace_id':'test-trace'})

    def test_only_public_documented_operations_are_imported(self):
        for row in self.coverage:
            for operation in row['operations']:
                if operation['disposition'] == 'schema_prepared':
                    self.assertIn(operation['api_id'], self.source['contracts'])
                    self.assertTrue(self.source['contracts'][operation['api_id']]['document_url'])
        self.assertEqual({'/aichat/conversations'}, set(self.plugins['deepseek']['paths']))
        self.assertNotIn('sora', self.plugins)
        self.assertNotIn('/minimax/regenerate', self.plugins['minimax']['paths'])
        self.assertNotIn('/minimax/prompt-enhancement', self.plugins['minimax']['paths'])

    def test_async_tools_have_result_retrieval(self):
        for key, definition in self.plugins.items():
            has_async = False
            for methods in definition['paths'].values():
                for operation in methods.values():
                    body = operation.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                    has_async |= 'async' in body.get('properties', {})
            if has_async:
                self.assertTrue(any(path.endswith('/tasks') or path == '/aichat2/conversations' for path in definition['paths']), key)
        self.assertIn('/maestro/tasks', self.plugins['maestro']['paths'])

    def test_starter_requests_and_listing_limits(self):
        starters = json.loads((ROOT / 'examples/catalog/starter-flows.json').read_text())
        for key, case in starters.items():
            if 'body' not in case:
                self.assertIn(case['status'], ['blocked_public_contract','awaiting_authorized_fixture'])
                continue
            body = self.plugins[key]['paths'][case['path']]['post']['requestBody']['content']['application/json']['schema']
            Draft4Validator(body).validate(case['body'])
        planned = json.loads((ROOT / 'examples/catalog/validation-cases.json').read_text())
        expected = {(row['key'], op['operation_id']) for row in self.coverage for op in row['operations'] if op['disposition'] == 'schema_prepared'}
        self.assertEqual(expected, {(case['service'], case['operation_id']) for case in planned})
        listings = json.loads((ROOT / 'listings.json').read_text())
        for listing in listings.values():
            self.assertLessEqual(len(listing['name']),30)
            self.assertLessEqual(len(listing['brief']),50)
            self.assertLessEqual(len(listing['about']),600)
            self.assertTrue(listing['scenarios'])
            self.assertNotIn('$t(',json.dumps(listing))

if __name__ == '__main__':
    unittest.main()
