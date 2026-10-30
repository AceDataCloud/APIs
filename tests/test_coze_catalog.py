import importlib.util
import json
import unittest
from pathlib import Path

from openapi_spec_validator import validate_spec
from openapi_schema_validator import OAS30Validator
from jsonschema import Draft4Validator, ValidationError

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
        self.assertEqual({x['id'] for x in self.source['services'] if x['type'] != 'Dataset' and builder.slug(x) not in {'aichat','digitalhuman','dreamina'}}, {x['service_id'] for x in self.coverage})
        self.assertEqual(len(self.coverage), len({x['key'] for x in self.coverage}))
        primary = [row for row in self.coverage if not row.get('variant_of')]
        self.assertEqual(len(primary), len({x['service_id'] for x in primary}))
        for row in self.coverage:
            self.assertTrue(row['name'])
            self.assertNotIn('AceData',row['name'])
            self.assertNotIn('_',row['name'])
            self.assertNotEqual('Dataset',row['service_type'])
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

    def test_gpt_image_is_separate_and_keeps_openai_capabilities(self):
        image=self.plugins['gpt-image']
        self.assertEqual({'/openai/images/generations','/openai/images/edits','/openai/tasks'},set(image['paths']))
        self.assertIn('/openai/chat/completions',self.plugins['openai']['paths'])
        for uri in ('/openai/images/generations','/openai/images/edits'):
            model=image['paths'][uri]['post']['requestBody']['content']['application/json']['schema']['properties']['model']
            self.assertEqual('gpt-image-2',model['default'])
            self.assertTrue(all(name.startswith('gpt-image') for name in model['enum']))
        projected=json.loads((ROOT/'imports/gpt-image.json').read_text())
        validate_spec(projected)
        result=projected['paths']['/openai/tasks']['post']['responses']['200']['content']['application/json']['schema']['properties']['response']['properties']
        self.assertIn('url',result['data']['items']['properties'])

    def test_image_quality_survives_building_and_projection(self):
        import yaml
        for route, api_id in (
            ('/openai/images/generations', '8f01fe72-8a3e-4872-8d8d-330cde179b3a'),
            ('/openai/images/edits', 'fb74083e-bb68-48d5-8ba6-b5a224400cd3'),
        ):
            contract = self.source['contracts'][api_id]
            source = contract['definition']['paths'][route]['post']
            canonical = self.plugins['openai']['paths'][route]['post']
            self.assertEqual(canonical, builder.build_operation(contract, route, 'post', source))
            for media in source['requestBody']['content'].values():
                quality = media['schema']['properties']['quality']
                self.assertTrue({'auto', 'low', 'medium', 'high', 'xhigh', 'max', 'standard'} <= set(quality['enum']))
                self.assertIn('Only `gpt-image-2.5-flare`', quality['description'])
                self.assertIn('`gpt-image-2.5-sunburst`', quality['description'])
                self.assertIn('`:official`', quality['description'])
                self.assertIn('actual token usage', quality['description'])
            for key in ('openai', 'gpt-image'):
                for folder in ('plugins', 'imports'):
                    with self.subTest(route=route, service=key, folder=folder):
                        document = json.loads((ROOT / folder / f'{key}.json').read_text())
                        self.assertEqual(document, yaml.safe_load((ROOT / folder / f'{key}.yaml').read_text()))
                        fields = document['paths'][route]['post']['requestBody']['content']['application/json']['schema']['properties']
                        self.assertEqual(canonical['requestBody']['content']['application/json']['schema']['properties']['quality'], fields['quality'])
                        for level in ('xhigh', 'max'):
                            OAS30Validator(fields['quality']).validate(level)
                        with self.assertRaises(ValidationError):
                            OAS30Validator(fields['quality']).validate('ultra')
                        self.assertTrue({'gpt-image-2:official', 'gpt-image-2.5-flare:official',
                                         'gpt-image-2.5-sunburst:official'} <= set(fields['model']['enum']))
                        if key == 'openai':
                            self.assertIn('gpt-image-2:reverse', fields['model']['enum'])
        self.assertEqual(self.plugins['openai'], yaml.safe_load((ROOT / 'image.yaml').read_text()))

    def test_suno_private_voice_cover_inputs_survive_building_and_projection(self):
        import yaml
        projected = json.loads((ROOT / 'imports/suno.json').read_text())
        for document, path in ((self.plugins['suno'], 'plugins/suno.yaml'),
                               (self.plugins['suno'], 'suno.yaml'),
                               (projected, 'imports/suno.yaml')):
            self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
        for route, api_id in (
            ('/suno/upload', '8823cd83-54f6-4ea8-979a-7fa448577186'),
            ('/suno/audios', '09a26295-5972-4392-9318-dcd9b218f90d'),
        ):
            contract = self.source['contracts'][api_id]
            operation = self.plugins['suno']['paths'][route]['post']
            self.assertEqual(operation, builder.build_operation(
                contract, route, 'post', contract['definition']['paths'][route]['post']))
            for document in (self.plugins['suno'], projected):
                with self.subTest(route=route, projected=document is projected):
                    body = document['paths'][route]['post']['requestBody']['content']['application/json']['schema']
                    persona = body['properties']['persona_id']
                    self.assertIn('same service channel', persona['description'])
                    if route == '/suno/upload':
                        self.assertNotIn('persona_id', body['required'])
                        self.assertEqual(1, persona['minLength'])
                        self.assertIn('only with mode=standard, not mode=enhanced', persona['description'])
                        OAS30Validator(body).validate({'audio_url': 'https://example.com/song.mp3'})
                        OAS30Validator(body).validate({'audio_url': 'https://example.com/song.mp3',
                                                      'mode': 'standard', 'persona_id': 'OWNED_VOICE_ID'})
                        with self.assertRaises(ValidationError):
                            OAS30Validator(persona).validate('')
                    else:
                        for text in ('cover / upload_cover', '/suno/upload', 'same persona_id',
                                     'returned audio_id', 'No additional vocal_gender'):
                            self.assertIn(text, persona['description'])
                        self.assertIn('upload_cover', body['properties']['action']['enum'])

    def test_suno_http_tasks_retain_music_and_export_results(self):
        projected=json.loads((ROOT/'imports/suno.json').read_text())
        validate_spec(projected)
        schema=projected['paths']['/suno/tasks']['post']['responses']['200']['content']['application/json']['schema']
        for props in (schema['properties'],schema['properties']['items']['items']['properties']):
            fields=props['response']['properties']
            self.assertTrue({'success','task_id','data','audio_url','error','cost'} <= set(fields))
            self.assertTrue({'id','audio_url','title','duration','state'} <= set(fields['data']['items']['properties']))
        lyrics=projected['paths']['/suno/lyrics']['post']
        fields=lyrics['responses']['200']['content']['application/json']['schema']['properties']['data']
        Draft4Validator(fields).validate({'title':'Morning','text':'Original lyrics','tags':['folk'],'status':'complete'})
        self.assertEqual(['default'],lyrics['requestBody']['content']['application/json']['schema']['properties']['model']['enum'])
        style=projected['paths']['/suno/style']['post']['responses']['200']['content']['application/json']['schema']['properties']['data']
        Draft4Validator(style).validate({'upsampled_tags':'Gentle acoustic folk with warm vocals.'})

    def test_suno_store_import_excludes_disabled_and_destructive_operations(self):
        import yaml
        projected = json.loads((ROOT / 'imports/suno.json').read_text())
        self.assertEqual(projected, yaml.safe_load((ROOT / 'imports/suno.yaml').read_text()))
        expected = {
            'generateMusic', 'cloneVoice', 'exportMp3', 'uploadAudio',
            'extractVocalStem', 'exportMidi', 'listPersonas', 'generateLyrics',
            'exportWav', 'getLyricTiming', 'refineMusicStyle', 'getTaskResults',
        }
        self.assertEqual(expected, {op['operationId'] for methods in projected['paths'].values()
                                    for op in methods.values()})
        for path, method in [('/suno/mp4', 'post'), ('/suno/custom-models', 'post'),
                             ('/suno/persona', 'post'), ('/suno/persona', 'delete'),
                             ('/suno/mashup-lyrics', 'post'), ('/suno/projects', 'post')]:
            self.assertIn(method, self.plugins['suno']['paths'][path])
            self.assertNotIn(method, projected['paths'].get(path, {}))
        for path, methods in projected['paths'].items():
            for method, op in methods.items():
                self.assertEqual(self.plugins['suno']['paths'][path][method]['parameters'],
                                 op['parameters'])

    def test_suno_negative_tags_guidance_survives_building_and_projection(self):
        import yaml
        canonical = self.plugins['suno']
        projected = json.loads((ROOT / 'imports/suno.json').read_text())
        for document, path in ((canonical, 'plugins/suno.yaml'),
                               (canonical, 'suno.yaml'),
                               (projected, 'imports/suno.yaml')):
            self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
        contract = self.source['contracts']['09a26295-5972-4392-9318-dcd9b218f90d']
        operation = canonical['paths']['/suno/audios']['post']
        self.assertEqual(operation, builder.build_operation(
            contract, '/suno/audios', 'post',
            contract['definition']['paths']['/suno/audios']['post']))
        tags = operation['requestBody']['content']['application/json']['schema']['properties']['negative_tags']
        imported = projected['paths']['/suno/audios']['post']['requestBody']['content']['application/json']['schema']['properties']['negative_tags']
        self.assertEqual(tags, imported)
        self.assertEqual('string', tags['type'])
        self.assertNotIn('maxLength', tags)
        self.assertIn('`custom` is `true`', tags['description'])
        self.assertIn('no fixed character limit', tags['description'])
        self.assertIn('overly long content may still fail to process', tags['description'])

    def test_kimi_k31_reasoning_survives_building_and_projection(self):
        import yaml
        route = '/kimi/chat/completions'
        canonical = self.plugins['kimi']
        projected = json.loads((ROOT / 'imports/kimi.json').read_text())
        contract = self.source['contracts']['5c4649ee-22c6-44ea-84d6-6ecc3674f998']
        operation = canonical['paths'][route]['post']
        self.assertEqual(operation, builder.build_operation(
            contract, route, 'post', contract['definition']['paths'][route]['post']))
        for document, path in ((canonical, 'plugins/kimi.yaml'),
                               (projected, 'imports/kimi.yaml')):
            with self.subTest(path=path):
                self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
                validate_spec(document)
                self.assertEqual({route}, set(document['paths']))
                body = document['paths'][route]['post']['requestBody']['content']['application/json']['schema']
                fields = body['properties']
                self.assertEqual(['kimi-k3.1-pro', 'kimi-k3', 'kimi-k2.6',
                                  'kimi-k2-thinking-turbo', 'kimi-k2.5', 'kimi-k2-thinking'],
                                 fields['model']['enum'])
                effort = fields['reasoning_effort']
                self.assertEqual(['low', 'high', 'max'], effort['enum'])
                self.assertEqual(['kimi-k3.1-pro', 'kimi-k3'], effort['x-allowed-models'])
                self.assertIn('use `max` for K3', effort['description'])
                self.assertIn('always enable reasoning', effort['description'])
                for model, levels in (('kimi-k3.1-pro', ('low', 'high', 'max')),
                                      ('kimi-k3', ('max',))):
                    for level in levels:
                        OAS30Validator(body).validate({
                            'model': model, 'messages': [{'role': 'user', 'content': 'Hello'}],
                            'reasoning_effort': level, 'stream': False,
                        })
                with self.assertRaises(ValidationError):
                    OAS30Validator(effort).validate('disabled')
                reasoning = fields['messages']['items']['properties']['reasoning_content']
                self.assertIn('K3.1 Pro or K3', reasoning['description'])
                self.assertIn('unchanged', reasoning['description'])
        message = operation['responses']['200']['content']['application/json']['schema']['properties']['choices']['items']['properties']['message']
        self.assertIn('K3.1 Pro or K3', message['properties']['reasoning_content']['description'])

    def test_opus_55_and_argon_models_survive_building_and_projection(self):
        import yaml
        cases = (
            ('claude', 'claude', '/v1/chat/completions',
             '6b2b437b-b6d5-466c-8750-b16650072593', 'claude-opus-5-5',
             ('claude-fable-5-1', 'claude-fable-5', 'claude-opus-5')),
            ('gemini', 'gemini-chat', '/gemini/chat/completions',
             '94b49b55-2ea8-4d46-a93c-eb308e1a52d5', 'gemini-4-argon',
             ('gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-2.5-flash')),
        )
        for key, projection, route, api_id, model, aliases in cases:
            contract = self.source['contracts'][api_id]
            canonical = self.plugins[key]
            operation = canonical['paths'][route]['post']
            self.assertEqual(operation, builder.build_operation(
                contract, route, 'post', contract['definition']['paths'][route]['post']))
            projected = json.loads((ROOT / 'imports' / f'{projection}.json').read_text())
            for document, path in ((canonical, f'plugins/{key}.yaml'),
                                   (projected, f'imports/{projection}.yaml')):
                with self.subTest(path=path):
                    self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
                    validate_spec(document)
                    body = document['paths'][route]['post']['requestBody']['content']['application/json']['schema']
                    models = body['properties']['model']['enum']
                    self.assertIn(model, models)
                    self.assertTrue(set(aliases) <= set(models))
                    self.assertEqual(operation['requestBody']['content']['application/json']['schema']['properties']['model']['enum'], models)
                    request = {'model': model, 'messages': [{'role': 'user', 'content': 'Hello'}],
                               'stream': False, 'max_tokens': 32768, 'n': 1}
                    OAS30Validator(body).validate(request)
                    with self.assertRaises(ValidationError):
                        OAS30Validator(body).validate({**request, 'model': 'unpublished-model'})
                    with self.assertRaises(ValidationError):
                        OAS30Validator(body).validate({**request, 'stream': True})

    def test_argon_native_model_enum_preserves_json_only_coze_scope(self):
        contract = self.source['contracts']['7a632630-eb9f-4776-b11c-8cc86ae250d7']
        for route, methods in contract['definition']['paths'].items():
            operation = methods['post']
            model = next(p['schema'] for p in operation['parameters'] if p['name'] == 'model')
            self.assertIn('gemini-4-argon', model['enum'])
            self.assertIn('gemini-3.8-flash', model['enum'])
            OAS30Validator(model).validate('gemini-4-argon')
            if 'streamGenerateContent' in route:
                self.assertNotIn(route, self.plugins['gemini']['paths'])
                continue
            built = builder.build_operation(contract, route, 'post', operation)
            self.assertEqual(built, self.plugins['gemini']['paths'][route]['post'])
            body = built['requestBody']['content']['application/json']['schema']
            OAS30Validator(body).validate({
                'contents': [{'role': 'user', 'parts': [{'text': 'Hello'}]}],
                'generationConfig': {'maxOutputTokens': 32768},
            })

    def test_kling_reference_video_billing_guidance_survives_building_and_projection(self):
        import yaml
        canonical = self.plugins['kling']
        projected = json.loads((ROOT / 'imports/kling.json').read_text())
        for document, path in ((canonical, 'plugins/kling.yaml'),
                               (canonical, 'kling.yaml'),
                               (projected, 'imports/kling.yaml')):
            self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
        contract = self.source['contracts']['29187cb2-1acb-43b8-baf5-3f3f709292eb']
        operation = canonical['paths']['/kling/videos']['post']
        self.assertEqual(operation, builder.build_operation(
            contract, '/kling/videos', 'post',
            contract['definition']['paths']['/kling/videos']['post']))
        video = operation['requestBody']['content']['application/json']['schema']['properties']['video_list']
        imported = projected['paths']['/kling/videos']['post']['requestBody']['content']['application/json']['schema']['properties']['video_list']
        self.assertEqual(video, imported)
        description = video['description']
        self.assertIn('separate billing tier', description)
        self.assertIn('Base editing is billed by actual output duration rounded to whole seconds', description)
        self.assertIn('feature reference uses the requested duration', description)
        self.assertIn('usage.reference_video_seconds', description)
        self.assertIn('Reference images alone do not trigger reference-video billing', description)
        self.assertIn('`generate_audio` must be `false`', description)

    def test_suno_projects_do_not_accept_batch_size(self):
        import yaml
        canonical = self.plugins['suno']
        for path in ('plugins/suno.yaml', 'suno.yaml'):
            self.assertEqual(canonical, yaml.safe_load((ROOT / path).read_text()))
        operation = canonical['paths']['/suno/projects']['post']
        contract = self.source['contracts']['ea455d55-7129-44ae-80a3-bf71aae074d8']
        self.assertEqual(operation, builder.build_operation(
            contract, '/suno/projects', 'post',
            contract['definition']['paths']['/suno/projects']['post']))
        body = operation['requestBody']['content']['application/json']['schema']
        branch = next(item for item in body['oneOf']
                      if item['properties']['action']['enum'] == ['generate_track'])
        self.assertNotIn('batch_size', body['properties'])
        self.assertNotIn('batch_size', branch['properties'])
        request = {
            'action': 'generate_track', 'id': 'owned-project', 'version_id': 'current-version',
            'source_audio_id': 'owned-source', 'render_audio_id': 'owned-render',
            'model': 'chirp-v4', 'start_seconds': 0, 'end_seconds': 8,
            'stem_control_tags': 'add Piano',
        }
        OAS30Validator(branch).validate(request)
        with self.assertRaises(ValidationError):
            OAS30Validator(branch).validate({**request, 'batch_size': 2})

    def test_prepared_video_forms_preserve_routes_auth_and_completed_media(self):
        import yaml
        for key in ('seedance', 'happyhorse'):
            projected = json.loads((ROOT / 'imports' / f'{key}.json').read_text())
            self.assertEqual(projected, yaml.safe_load((ROOT / 'imports' / f'{key}.yaml').read_text()))
            validate_spec(projected)
            self.assertEqual({f'/{key}/videos', f'/{key}/tasks'}, set(projected['paths']))
            for path, methods in projected['paths'].items():
                for method, op in methods.items():
                    self.assertEqual(self.plugins[key]['paths'][path][method]['parameters'],
                                     op['parameters'])
            task = projected['paths'][f'/{key}/tasks']['post']['responses']['200']['content']['application/json']['schema']
            for container in (task['properties'], task['properties']['items']['items']['properties']):
                props = container['response']['properties']
                self.assertTrue({'success', 'task_id', 'data', 'error'} <= set(props))
                if key == 'seedance':
                    self.assertIn('video_url', props['data']['properties'])
                    self.assertIn('video_url', props['data']['properties']['content']['properties'])
                else:
                    self.assertIn('video_url', props['data']['items']['properties'])
            body = projected['paths'][f'/{key}/videos']['post']['requestBody']['content']['application/json']['schema']
            self.assertNotIn('callback_url', body['properties'])
            if key == 'seedance':
                item = body['properties']['content']['items']
                self.assertEqual(['text'], item['properties']['type']['enum'])
                self.assertEqual({'type', 'text'}, set(item['required']))
                self.assertNotIn('tools', body['properties'])

    def test_service_discovery_uses_independent_brands_and_known_store_ids(self):
        discovery = json.loads((ROOT / 'catalog/service-discovery.json').read_text())['services']
        listings = json.loads((ROOT / 'listings.json').read_text())
        self.assertEqual({'suno', 'seedance', 'happyhorse', 'gpt-image', 'nano-banana'}, set(discovery))
        for key, prepared in discovery.items():
            listing = listings[key]
            self.assertEqual(prepared['service_name']+' by Ace Data Cloud', listing['name'])
            self.assertIn('Ace Data Cloud integration', listing['description'])
            self.assertEqual(prepared['category'], listing['category'])
            if key in {'seedance', 'happyhorse'}:
                self.assertIsNone(prepared['plugin_id'])
                self.assertIsNone(prepared['official_listing'])
            else:
                self.assertTrue(prepared['official_listing'].endswith(prepared['plugin_id']))
        self.assertEqual(12, discovery['suno']['prepared_tools'])

    def test_full_nano_banana_form_preserves_image_task_results(self):
        import yaml
        projected = json.loads((ROOT / 'imports/nano-banana.json').read_text())
        validate_spec(projected)
        self.assertEqual(projected, yaml.safe_load((ROOT / 'imports/nano-banana.yaml').read_text()))
        self.assertEqual(set(self.plugins['nano-banana']['paths']), set(projected['paths']))
        output = projected['paths']['/nano-banana/tasks']['post']['responses']['200']['content']['application/json']['schema']
        fields = output['properties']['response']['properties']['data']['items']['properties']
        self.assertIn('image_url', fields)
        for props in (output['properties'], output['properties']['items']['items']['properties']):
            self.assertEqual({'code', 'message'}, set(props['response']['properties']['error']['properties']))

    def test_new_store_forms_omit_numeric_formats_rejected_by_editor(self):
        def check(value):
            if isinstance(value, dict):
                if value.get('type') in ('number', 'integer'):
                    self.assertNotIn(value.get('format'), {'double', 'float', 'int32', 'int64'})
                for child in value.values():
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)
        for key in ('seedance', 'happyhorse', 'nano-banana'):
            projected = json.loads((ROOT / 'imports' / f'{key}.json').read_text())
            check(projected)
            props = projected['paths'][f'/{key}/tasks']['post']['responses']['200']['content']['application/json']['schema']['properties']
            for name in ('elapsed', 'created_at', 'started_at', 'finished_at'):
                self.assertEqual('number', props[name]['type'])
            canonical = self.plugins[key]['paths'][f'/{key}/tasks']['post']['responses']['200']['content']['application/json']['schema']
            self.assertEqual('double', canonical['properties']['created_at']['format'])

    def test_compatibility_imports_preserve_routes_auth_and_file_parity(self):
        import yaml
        for key in ('claude', 'openai', 'kling', 'serp', 'kimi'):
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

    def test_coze_chat_projection_omits_inactive_required_children(self):
        # Coze validates children of optional objects even when the object is unused.
        # Keep these conditional inputs in the canonical API contract only.
        for key, path in [('openai', '/openai/chat/completions'),
                          ('claude', '/v1/chat/completions'),
                          ('kimi', '/kimi/chat/completions')]:
            projected = json.loads((ROOT / 'imports' / f'{key}.json').read_text())
            body = projected['paths'][path]['post']['requestBody']['content']['application/json']['schema']
            canonical = self.plugins[key]['paths'][path]['post']['requestBody']['content']['application/json']['schema']
            inactive = {'audio', 'prediction', 'stream_options', 'web_search_options'}
            self.assertTrue(inactive <= set(canonical['properties']))
            self.assertFalse(inactive & set(body['properties']))
            self.assertTrue({'model', 'messages'} <= set(body['properties']))
            canonical_message = canonical['properties']['messages']['items']
            projected_message = body['properties']['messages']['items']
            self.assertIn('tool_calls', canonical_message['properties'])
            self.assertNotIn('tool_calls', projected_message['properties'])
            self.assertTrue({'role', 'content'} <= set(projected_message['properties']))

    def test_partial_chat_imports_leave_other_plugin_routes_untouched(self):
        import yaml
        for key in ('gemini', 'grok', 'glm'):
            path = f'/{key}/chat/completions'
            projected = json.loads((ROOT / 'imports' / f'{key}-chat.json').read_text())
            self.assertEqual(projected, yaml.safe_load((ROOT / 'imports' / f'{key}-chat.yaml').read_text()))
            validate_spec(projected)
            self.assertEqual({path}, set(projected['paths']))
            self.assertEqual(self.plugins[key]['paths'][path]['post']['parameters'],
                             projected['paths'][path]['post']['parameters'])
            body = projected['paths'][path]['post']['requestBody']['content']['application/json']['schema']
            self.assertTrue({'model', 'messages'} <= set(body['properties']))
            self.assertNotIn('tool_calls', body['properties']['messages']['items']['properties'])

    def test_fish_tts_import_supports_plain_speech_without_reference_audio(self):
        projected = json.loads((ROOT / 'imports/fish-tts.json').read_text())
        validate_spec(projected)
        self.assertEqual({'/fish/tts'}, set(projected['paths']))
        body = projected['paths']['/fish/tts']['post']['requestBody']['content']['application/json']['schema']
        canonical = self.plugins['fish']['paths']['/fish/tts']['post']['requestBody']['content']['application/json']['schema']
        self.assertIn('references', canonical['properties'])
        self.assertNotIn('references', body['properties'])
        self.assertIn('text', body['required'])
        output = projected['paths']['/fish/tts']['post']['responses']['200']['content']['application/json']['schema']
        self.assertTrue({'task_id', 'started_at', 'audio_url'} <= set(output['properties']))

    def test_localization_markdown_import_has_a_concrete_input_type(self):
        projected = json.loads((ROOT / 'imports/localization-md.json').read_text())
        validate_spec(projected)
        body = projected['paths']['/localization/translate']['post']['requestBody']['content']['application/json']['schema']
        self.assertEqual('string', body['properties']['input']['type'])
        self.assertEqual(['md'], body['properties']['extension']['enum'])
        self.assertTrue({'input', 'locale', 'extension'} <= set(body['required']))
        output = projected['paths']['/localization/translate']['post']['responses']['200']['content']['application/json']['schema']
        self.assertEqual('string', output['properties']['data']['type'])

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

    def test_web_extractor_task_result_retains_content_fields(self):
        operation = self.plugins['webextrator']['paths']['/webextrator/tasks']['post']
        schema = operation['responses']['200']['content']['application/json']['schema']
        fields = schema['properties']['response']['properties']
        self.assertTrue({'markdown', 'text', 'title', 'kind'} <= set(fields))
        batch_fields = schema['properties']['items']['items']['properties']['response']['properties']
        self.assertTrue({'markdown', 'text', 'title', 'kind'} <= set(batch_fields))
        self.assertNotIn('oneOf', schema)

    def test_image_task_result_retains_generated_image_url(self):
        for key in ('nano-banana', 'qwen-image'):
            schema = self.plugins[key]['paths'][f'/{key}/tasks']['post']['responses']['200']['content']['application/json']['schema']
            for props in (schema['properties'], schema['properties']['items']['items']['properties']):
                image = props['response']['properties']['data']['items']['properties']['image_url']
                self.assertEqual('string', image['type'])
            self.assertNotIn('oneOf', schema)
            projected = json.loads((ROOT / 'imports' / f'{key}-task.json').read_text())
            self.assertEqual({f'/{key}/tasks'}, set(projected['paths']))
            validate_spec(projected)

    def test_error_union_accepts_a_real_error_shape(self):
        operation=self.plugins['shorturl']['paths']['/shorturl']['post']
        schema=operation['responses']['401']['content']['application/json']['schema']
        Draft4Validator(schema).validate({'error':{'code':'invalid_token','message':'Invalid credential.'},'trace_id':'test-trace'})

    def test_grok_task_result_retains_video_and_error_fields(self):
        projected = json.loads((ROOT / 'imports/grok-task.json').read_text())
        self.assertEqual({'/grok/tasks'}, set(projected['paths']))
        validate_spec(projected)
        schema = projected['paths']['/grok/tasks']['post']['responses']['200']['content']['application/json']['schema']
        self.assertNotIn('oneOf', schema)
        for props in (schema['properties'], schema['properties']['items']['items']['properties']):
            result = props['response']['properties']
            video = result['data']['items']['properties']
            self.assertEqual('string', video['video_url']['type'])
            self.assertEqual('string', video['state']['type'])
            self.assertEqual('number', video['duration']['type'])
            self.assertTrue({'code', 'message'} <= set(result['error']['properties']))

    def test_openai_task_import_retains_generated_and_edited_images(self):
        for filename in ('openai', 'openai-task'):
            projected = json.loads((ROOT / 'imports' / f'{filename}.json').read_text())
            validate_spec(projected)
            schema = projected['paths']['/openai/tasks']['post']['responses']['200']['content']['application/json']['schema']
            self.assertTrue({'count_relation', 'has_more', 'count_is_exact'} <= set(schema['properties']))
            for props in (schema['properties'], schema['properties']['items']['items']['properties']):
                result = props['response']['properties']
                image = result['data']['items']['properties']
                self.assertTrue({'url', 'b64_json', 'revised_prompt'} <= set(image))
                self.assertTrue({'success', 'model', 'cost', 'error'} <= set(result))

    def test_gemini_video_task_import_retains_completed_video(self):
        projected = json.loads((ROOT / 'imports/gemini-task.json').read_text())
        validate_spec(projected)
        schema = projected['paths']['/gemini/tasks']['post']['responses']['200']['content']['application/json']['schema']
        for props in (schema['properties'], schema['properties']['items']['items']['properties']):
            video = props['response']['properties']['data']['items']['properties']
            self.assertTrue({'video_url', 'state', 'aspect_ratio', 'prompt'} <= set(video))

    def test_fish_voice_listing_retains_identity_and_pagination(self):
        projected = json.loads((ROOT / 'imports/fish-voices.json').read_text())
        self.assertEqual({'/fish/model'}, set(projected['paths']))
        self.assertEqual({'get'}, set(projected['paths']['/fish/model']))
        validate_spec(projected)
        schema = projected['paths']['/fish/model']['get']['responses']['200']['content']['application/json']['schema']
        fields = schema['properties']['items']['items']['properties']
        self.assertTrue({'_id', 'title', 'state', 'licensed', 'visibility'} <= set(fields))
        self.assertTrue({'has_more', 'total_is_exact', 'window_limited', 'max_offset'} <= set(schema['properties']))
        # A partial result window must not lose the signal that total is a bound.
        Draft4Validator(schema).validate({
            'items':[{'_id':'sample-voice','title':'Demo','licensed':False,'state':'trained'}],
            'total':1000,'total_is_exact':False,'has_more':True,
            'window_limited':True,'max_offset':1000,'accessible_upper_bound':1000,
        })

    def test_fish_model_contract_updates_survive_building_and_projection(self):
        import yaml
        canonical = self.plugins['fish']
        projected = json.loads((ROOT / 'imports/fish-voices.json').read_text())
        for document, path in ((canonical, 'plugins/fish.yaml'),
                               (projected, 'imports/fish-voices.yaml')):
            self.assertEqual(document, yaml.safe_load((ROOT / path).read_text()))
        listing = canonical['paths']['/fish/model']['get']
        self.assertEqual(listing, projected['paths']['/fish/model']['get'])
        for api_id, method in (('0a2c983b-e20f-5926-a45f-07b61373617d', 'get'),
                               ('82dcabe9-b1a3-541f-80f1-decb183b920c', 'post')):
            contract = self.source['contracts'][api_id]
            self.assertEqual(canonical['paths']['/fish/model'][method], builder.build_operation(
                contract, '/fish/model', method,
                contract['definition']['paths']['/fish/model'][method]))
        params = {item['name']: item for item in listing['parameters']}
        self.assertIn('across its API tokens', params['self']['description'])
        self.assertIn('not public voice access', params['self']['description'])
        self.assertIn('not supported with `self=true`', params['title_language']['description'])
        self.assertIn('`created_at` and `task_count`', params['sort_by']['description'])
        schema = listing['responses']['200']['content']['application/json']['schema']
        self.assertTrue(schema['properties']['has_more']['nullable'])
        for value in (True, False, None):
            OAS30Validator(schema).validate({'total': 0, 'items': [], 'has_more': value})
        with self.assertRaises(ValidationError):
            OAS30Validator(schema).validate({'has_more': 'false'})
        creation = canonical['paths']['/fish/model']['post']
        self.assertIn('201', creation['responses'])
        self.assertNotIn('200', creation['responses'])
        visibility = creation['responses']['201']['content']['application/json']['schema']['properties']['visibility']
        self.assertIn('saved publicly', visibility['description'])
        self.assertIn('does not restrict access', visibility['description'])

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
        for case in planned:
            if case['method'] == 'DELETE':
                self.assertTrue(case['special_authorization'])
                self.assertEqual('not_run', case['status'])
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
