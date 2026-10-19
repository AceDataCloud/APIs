"""Execute exported expressions with Node, without service requests."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = json.loads((ROOT / 'workflows/n8n/search-summary.json').read_text())
NODES = {n['name']: n for n in WORKFLOW['nodes']}
EVALUATOR = """
let raw = ''; process.stdin.on('data', c => raw += c);
process.stdin.on('end', () => {
  const {expression, input, context} = JSON.parse(raw);
  const lookup = name => ({first: () => ({json: context[name]})});
  const result = new Function('$json', '$', 'return (' + expression + ')')(input, lookup);
  process.stdout.write(JSON.stringify(result));
});
"""


def evaluate(expression, value, context=None):
    return json.loads(subprocess.check_output(
        ['node', '-e', EVALUATOR], text=True,
        input=json.dumps(dict(expression=expression[3:-2].strip(), input=value,
                             context=context or {}))))


def condition(name, value):
    item = NODES[name]['parameters']['conditions']['conditions'][0]
    return evaluate(item['leftValue'], value) == item['rightValue']


def assignment(name, field):
    return next(a['value'] for a in NODES[name]['parameters']['assignments']['assignments']
                if a['name'] == field)


class SearchSummaryTest(unittest.TestCase):
    def setUp(self):
        self.valid = dict(query='Research question', number=5,
                          model='explicit-chat-model', max_tokens=512)

    def test_configuration_is_required_before_search(self):
        exported = {a['name']: a['value'] for a in
                    NODES['Set research input']['parameters']['assignments']['assignments']}
        self.assertEqual(exported['model'], '')
        self.assertFalse(condition('Validate research input', exported))
        self.assertTrue(condition('Validate research input', self.valid))
        for field, values in dict(query=['', ' ', 'x'*501, None], number=[0, 11, 1.5, '5'],
                                  model=['', ' model', 'x\n', None],
                                  max_tokens=[31, 1025, 33.5, '512']).items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.assertFalse(condition('Validate research input', {**self.valid, field: value}))

    def test_fixed_hosts_no_retry_or_redirects(self):
        for name, endpoint, timeout in [
            ('Search with Ace Data Cloud', '/serp/google', 60000),
            ('Summarize with Ace Data Cloud', '/v1/chat/completions', 120000),
        ]:
            n = NODES[name]; p = n['parameters']
            self.assertEqual(p['url'], 'https://api.acedata.cloud' + endpoint)
            self.assertEqual(p['method'], 'POST')
            self.assertEqual(p['genericAuthType'], 'httpHeaderAuth')
            self.assertEqual(p['authentication'], 'genericCredentialType')
            self.assertEqual(p['options']['timeout'], timeout)
            self.assertFalse(p['options']['redirect']['redirect']['followRedirects'])
            self.assertFalse(n['retryOnFail'])

    def test_sources_are_usable_and_bounded(self):
        expr = assignment('Select bounded sources', 'sources')
        context = {'Set research input': {**self.valid, 'number': 2}}
        for body in [None, {}, {'organic': {}}, {'organic': []},
                     {'organic': [None, {}, dict(title='bad', link='javascript:x', snippet='x')]}]:
            sources = evaluate(expr, {'body': body}, context)
            self.assertEqual(sources, [])
            self.assertFalse(condition('Has usable sources', {'sources': sources}))
        source = dict(title='t'*300, link='https://example.com/', snippet='s'*2000, unrelated='drop')
        sources = evaluate(expr, {'body': {'organic': [source]*20}}, context)
        self.assertEqual(len(sources), 2)
        self.assertEqual(len(sources[0]['title']), 200)
        self.assertEqual(len(sources[0]['snippet']), 1000)
        self.assertEqual(set(sources[0]), {'index', 'title', 'link', 'snippet'})
        messages = evaluate(assignment('Build grounded summary request', 'messages'),
                            {'sources': sources}, context)
        self.assertIn('untrusted data', messages[0]['content'])
        self.assertEqual(json.loads(messages[1]['content'])['sources'], sources)

    def test_payload_preserves_exact_model_and_output_cap(self):
        body = evaluate(NODES['Summarize with Ace Data Cloud']['parameters']['body'],
                        dict(model='exact-selected-id', messages=[], max_tokens=64))
        payload = json.loads(body)
        self.assertEqual(payload['model'], 'exact-selected-id')
        self.assertEqual(payload['max_tokens'], 64)
        self.assertFalse(payload['stream'])

    def test_http_and_completion_failures_fail_closed(self):
        for name in ('Search succeeded', 'Summary succeeded'):
            for status in (200, 301, 403, 429, 500):
                self.assertEqual(condition(name, {'statusCode': status}), status == 200)
        valid = dict(model='resolved-id', choices=[dict(finish_reason='stop', message=dict(content='Answer [1]'))])
        self.assertTrue(condition('Summary is complete', {'body': valid}))
        for body in [None, {}, dict(choices=[]), {**valid, 'model': ''},
                     {**valid, 'choices': [dict(finish_reason='length', message=dict(content='partial'))]},
                     {**valid, 'choices': [dict(finish_reason='stop', message=dict(content=' '))]}]:
            self.assertFalse(condition('Summary is complete', {'body': body}))

    def test_graph_has_no_resubmission_and_explicit_failures(self):
        for source, targets in {
            'Set research input': ['Validate research input'],
            'Validate research input': ['Search with Ace Data Cloud', 'Stop on invalid input'],
            'Search succeeded': ['Select bounded sources', 'Stop on search error'],
            'Has usable sources': ['Build grounded summary request', 'Stop on empty search'],
            'Summary succeeded': ['Summary is complete', 'Stop on summary error'],
            'Summary is complete': ['Return structured report', 'Stop on incomplete summary'],
        }.items():
            self.assertEqual([e[0]['node'] for e in WORKFLOW['connections'][source]['main']], targets)
        visiting, visited = set(), set()

        def walk(name):
            self.assertNotIn(name, visiting)
            if name in visited:
                return
            visiting.add(name)
            for edges in WORKFLOW['connections'].get(name, {}).get('main', []):
                for edge in edges:
                    walk(edge['node'])
            visiting.remove(name); visited.add(name)
        walk('Run manually')
        self.assertEqual(visited, set(NODES))
        for name, node in NODES.items():
            if node['type'] == 'n8n-nodes-base.stopAndError':
                self.assertNotIn(name, WORKFLOW['connections'])

    def test_export_and_onboarding(self):
        self.assertFalse(WORKFLOW['active'])
        self.assertEqual(WORKFLOW['pinData'], {})
        self.assertEqual(WORKFLOW['id'], 'acedata-search-summary-v1')
        for node in NODES.values():
            self.assertNotIn('credentials', node)
        self.assertNotIn('Bearer ', json.dumps(WORKFLOW))
        text = (ROOT / 'workflows/n8n/search-summary.md').read_text()
        for required in ('two billable API calls', 'Allowed APIs', 'can overwrite an existing workflow',
                         'GoogleSearchN8N', 'AceChatN8N', 'not a guarantee'):
            self.assertIn(required, text)
        import re
        from urllib.parse import parse_qs, urlsplit
        urls = re.findall(r'https://platform\.acedata\.cloud/[^)\s]+', text)
        self.assertTrue(urls)
        for url in urls:
            query = parse_qs(urlsplit(url).query)
            self.assertEqual(query['utm_source'], ['opensource'])
            self.assertEqual(query['utm_medium'], ['referral'])
            self.assertEqual(query['utm_campaign'], ['evergreen'])
            self.assertTrue(query['utm_content'][0])
