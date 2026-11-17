"""The new service is a candidate until deployed, never a historic live snapshot."""
import json
from pathlib import Path
import unittest
import yaml
from openapi_spec_validator import validate_spec

ROOT = Path(__file__).resolve().parents[1]

class AceMusicCandidateTests(unittest.TestCase):
    def test_import_contract_preserves_models_tasks_and_private_auth(self):
        path = ROOT / 'coze/candidates/acemusic/openapi.json'
        spec = json.loads(path.read_text())
        self.assertEqual(spec, yaml.safe_load(path.with_suffix('.yaml').read_text()))
        validate_spec(spec)
        self.assertEqual(set(spec['paths']), {'/acemusic/audios', '/acemusic/lyrics', '/acemusic/tasks'})
        for route, methods in spec['paths'].items():
            operation = methods['post']
            self.assertTrue(any(p['name'] == 'Authorization' and p['required'] for p in operation['parameters']))
            self.assertNotIn('Bearer hk-', json.dumps(operation))
        self.assertIn('acemusic-v1.1', json.dumps(spec))
        self.assertIn('retrieve_batch', json.dumps(spec))
        self.assertIn('partial_failed', json.dumps(spec))
