"""ACE Music original candidate and current Coze editor import contracts."""
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

    def test_editor_import_and_mcp_discovery_are_distinct(self):
        coze = ROOT / 'coze'
        spec = json.loads((coze / 'imports/acemusic.json').read_text())
        self.assertEqual(spec, yaml.safe_load((coze / 'imports/acemusic.yaml').read_text()))
        validate_spec(spec)
        operations = {path: methods['post'] for path, methods in spec['paths'].items()}
        self.assertEqual({op['operationId'] for op in operations.values()}, {'generateMusic', 'generateLyrics', 'getTaskResults'})
        for op in operations.values():
            auth, = [param for param in op['parameters'] if param['name'] == 'Authorization']
            self.assertTrue(auth['required'])
            self.assertNotIn('default', auth['schema'])
            body = json.dumps(op)
            for unsupported in ('"allOf":', '"oneOf":', '"anyOf":', '"format": "uri"'):
                self.assertNotIn(unsupported, body)
        response = operations['/acemusic/tasks']['responses']['200']['content']['application/json']['schema']['properties']
        for row in (response, response['items']['items']['properties']):
            fields = row['response']['properties']['data']['items']['properties']
            self.assertTrue({'audio_url', 'id', 'text', 'title'} <= fields.keys())
        mcp = json.loads((coze / 'mcp-plugins/acemusic.json').read_text())
        self.assertEqual(mcp['server_url'], 'https://acemusic.mcp.acedata.cloud/mcp')
        self.assertEqual(len(set(mcp['expected_tool_names'])), mcp['expected_tool_count'])
        self.assertTrue({'acemusic_cover_audio', 'acemusic_upload_audio', 'acemusic_mashup_audio'} <= set(mcp['expected_tool_names']))
