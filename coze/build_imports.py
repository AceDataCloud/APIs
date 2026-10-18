#!/usr/bin/env python3
"""Project standard API schemas to Coze's single-type parameter editor.

Canonical API constraints remain in plugins/. This projection does not alter
endpoints, billing, authentication or server-side validation. Differences are
recorded for review, never presented as additional API capabilities.
"""
from __future__ import annotations
import copy,json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent
notes=[]

def concrete_objects(value):
    """Coze's importer cannot convert boolean additionalProperties to a field."""
    if isinstance(value,dict):
        return {k:concrete_objects(v) for k,v in value.items() if k != 'additionalProperties'}
    if isinstance(value,list):
        return [concrete_objects(v) for v in value]
    return value

def kind(s):
    if s.get('type'):return s['type']
    if 'properties' in s or 'additionalProperties' in s:return 'object'
    if 'items' in s:return 'array'
    if s.get('enum'):
        v=next((v for v in s['enum'] if v is not None),'')
        return 'boolean' if isinstance(v,bool) else 'integer' if isinstance(v,int) else 'number' if isinstance(v,float) else 'string'
    return None


def project(s,location):
    if not isinstance(s,dict):return s
    s=copy.deepcopy(s)
    branches=s.pop('oneOf',None) or s.pop('anyOf',None)
    s.pop('oneOf',None);s.pop('anyOf',None)
    if branches:
        variants=[project(v,location) for v in branches]
        base=kind(s);types=list(dict.fromkeys(kind(v) for v in variants if kind(v)))
        # Retain an explicit base type. For heterogeneous content, use the
        # ordinary text representation; image lists use the array form.
        chosen=base or ('array' if location.endswith('/image') and 'array' in types else 'string' if 'string' in types else 'integer' if 'integer' in types else 'number' if 'number' in types else types[0] if types else 'object')
        if len(types)>1:
            if set(types)=={'integer','number'}:chosen='number'
            elif set(types)=={'integer','string'}:chosen='integer'
            notes.append({'field':location,'kind':'representation','api_types':types,'coze_type':chosen})
        candidates=[v for v in variants if kind(v)==chosen or (chosen=='number' and kind(v)=='integer')]
        s['type']=chosen
        if chosen=='object':
            props=copy.deepcopy(s.get('properties',{}));required=None
            for v in candidates:
                r=set(v.get('required',[]));required=r if required is None else required&r
                for k,val in v.get('properties',{}).items():
                    if k not in props:props[k]=val
                    elif props[k]!=val:props[k]=project({'anyOf':[props[k],val]},location+'/'+k)
            s['properties']=props
            req=set(s.get('required',[]))|(required or set())
            if req:s['required']=sorted(req)
        elif chosen=='array':
            options=[v['items'] for v in candidates if 'items' in v]
            if 'items' not in s and options:s['items']=options[0] if len(options)==1 else project({'anyOf':options},location+'/items')
        else:
            if candidates:
                for k,v in candidates[0].items():
                    if k not in s:s[k]=v
                enums=[v.get('enum') for v in candidates]
                if enums and all(enums):s['enum']=list(dict.fromkeys(x for enum in enums for x in enum))
    if 'allOf' in s:
        s.pop('allOf');notes.append({'field':location,'kind':'conditional_constraints','validation':'The API remains authoritative; original constraints are retained in plugins/.'})
    s.pop('not',None);s.pop('discriminator',None)
    if 'type' not in s:s['type']=kind(s) or 'object'
    if s.get('default') is None:s.pop('default',None)
    if 'properties' in s:s['properties']={k:project(v,location+'/'+k) for k,v in s['properties'].items()}
    if 'items' in s:s['items']=project(s['items'],location+'/items')
    if isinstance(s.get('additionalProperties'),dict):s['additionalProperties']=project(s['additionalProperties'],location+'/additionalProperties')
    # Never retain an incompatible default from an alternative representation.
    if 'default' in s:
        value=s['default'];ok={'string':isinstance(value,str),'integer':isinstance(value,int) and not isinstance(value,bool),'number':isinstance(value,(int,float)) and not isinstance(value,bool),'boolean':isinstance(value,bool),'array':isinstance(value,list),'object':isinstance(value,dict)}
        if not ok.get(s['type'],True):s.pop('default')
    return s


def main():
    target=ROOT/'imports';target.mkdir(exist_ok=True);report={}
    overrides=json.loads((ROOT/'catalog/coze-compatibility-overrides.json').read_text())
    for path in sorted((ROOT/'plugins').glob('*.json')):
        if path.stem not in overrides: continue
        notes.clear();doc=json.loads(path.read_text())
        for uri,methods in doc['paths'].items():
            for method,op in methods.items():
                loc=method.upper()+' '+uri
                for p in op.get('parameters',[]):
                    if 'schema' in p:p['schema']=project(p['schema'],loc+'/header/'+p['name'])
                for media in op.get('requestBody',{}).get('content',{}).values():
                    if 'schema' in media:media['schema']=project(media['schema'],loc+'/request')
                for status,r in op.get('responses',{}).items():
                    for media in r.get('content',{}).values():
                        if 'schema' in media:media['schema']=project(media['schema'],loc+'/response/'+status)
                override=overrides[path.stem][uri]
                body=op.get('requestBody',{}).get('content',{}).get('application/json',{}).get('schema',{})
                props=body.get('properties',{})
                for name in list(props):
                    if name not in override['request_fields']:
                        assert name not in body.get('required',[]), 'Never remove a required API input'
                        del props[name]
                        notes.append({'field':loc+'/request/'+name,'kind':'omitted_optional_input','reason':'Opaque object unsupported by Coze editor; canonical contract retains it.'})
                if path.stem in {'openai','claude','kimi'} and uri.endswith('/chat/completions'):
                    message=props['messages']['items']
                    assert 'tool_calls' not in message.get('required',[])
                    message['properties'].pop('tool_calls',None)
                    notes.append({'field':loc+'/request/messages/items/tool_calls','kind':'omitted_optional_input','reason':'Coze requires nested tool-call fields even for a plain user message; canonical contract retains them.'})
                op['responses']=copy.deepcopy(override['responses'])
                if path.stem=='openai' and uri=='/openai/tasks':
                    # Older import overrides omit the dynamic task response.
                    # Restore it without replacing the override's pagination fields.
                    canonical=json.loads(path.read_text())['paths'][uri][method]
                    source=canonical['responses']['200']['content']['application/json']['schema']['properties']
                    output=op['responses']['200']['content']['application/json']['schema']['properties']
                    output['response']=copy.deepcopy(source['response'])
                    output['items']['items']['properties']['response']=copy.deepcopy(source['items']['items']['properties']['response'])
                if path.stem in {'claude','serp'}:
                    op['responses']={'200':op['responses']['200']}
                    def clean(value):
                        if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k not in {'additionalProperties','maxItems','minItems','nullable','externalDocs'}}
                        if isinstance(value,list):return [clean(v) for v in value]
                        return value
                    methods[method]=op=clean(op)
                limits=[n for n in notes if n['field'].startswith(loc+'/request') and n['kind'] in {'representation','omitted_optional_input'}]
                op['description']+=' This Coze form uses explicit parameter types. Model/action requirements in the linked API guide still apply.'
                if limits:op['description']+=' Coze form limitations: some union inputs use one representation and optional opaque objects are omitted; see compatibility notes. Text-message content is supported where the form uses string.'
        report[path.stem]=copy.deepcopy(notes)
        (target/path.name).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
        (target/(path.stem+'.yaml')).write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    # These plugins also contain non-chat tools. Reimport only the chat route
    # so a Coze text-form fix does not replace their unrelated draft tools.
    chat_fields=set(overrides['openai']['/openai/chat/completions']['request_fields'])
    chat_response=overrides['openai']['/openai/chat/completions']['responses']
    for key in ('gemini','grok','glm'):
        uri=f'/{key}/chat/completions'
        doc=json.loads((ROOT/'plugins'/f'{key}.json').read_text())
        doc['paths']={uri:doc['paths'][uri]}
        op=doc['paths'][uri]['post']
        body=op['requestBody']['content']['application/json']['schema']
        body=project(body,'POST '+uri+'/request')
        body['properties']={k:v for k,v in body['properties'].items() if k in chat_fields}
        assert set(body.get('required',[])) <= set(body['properties'])
        message=body['properties']['messages']['items']
        assert 'tool_calls' not in message.get('required',[])
        message['properties'].pop('tool_calls',None)
        op['requestBody']['content']['application/json']['schema']=body
        op['responses']=copy.deepcopy(chat_response)
        op['description']+=' This Coze text-chat form omits inactive optional objects and message tool-call children. The canonical API contract retains them.'
        report[key+'-chat']=[{'field':'POST '+uri+'/request/messages/items/tool_calls','kind':'omitted_optional_input','reason':'Coze requires nested tool-call fields even for plain user messages.'}]
        (target/f'{key}-chat.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
        (target/f'{key}-chat.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    for key in ('nano-banana','qwen-image','grok','gemini','openai'):
        uri=f'/{key}/tasks'
        doc=json.loads(((target if key=='openai' else ROOT/'plugins')/f'{key}.json').read_text())
        doc['paths']={uri:doc['paths'][uri]}
        media_field='video_url' if key in {'grok','gemini'} else 'url' if key=='openai' else 'image_url'
        report[key+'-task']=[{'field':'POST '+uri+'/response/data/items/'+media_field,'kind':'declared_output','reason':'Coze drops undeclared media URLs from dynamic task results.'}]
        (target/f'{key}-task.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
        (target/f'{key}-task.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    doc=json.loads((ROOT/'plugins/fish.json').read_text())
    voice_doc=copy.deepcopy(doc)
    voice_doc['paths']={'/fish/model':{'get':voice_doc['paths']['/fish/model']['get']}}
    report['fish-voices']=[{'field':'GET /fish/model/response/items','kind':'declared_output','reason':'Coze drops undeclared voice IDs and metadata; pagination includes lower-bound totals.'}]
    (target/'fish-voices.json').write_text(json.dumps(voice_doc,ensure_ascii=False,indent=2)+'\n')
    (target/'fish-voices.yaml').write_text(yaml.safe_dump(voice_doc,allow_unicode=True,sort_keys=False,width=100))
    uri='/fish/tts'
    doc['paths']={uri:doc['paths'][uri]}
    body=doc['paths'][uri]['post']['requestBody']['content']['application/json']['schema']
    assert 'references' not in body.get('required',[])
    body['properties'].pop('references',None)
    doc['paths'][uri]['post']['description']+=' Inline reference audio is omitted from this Coze form because it requires child fields even for ordinary TTS. The canonical contract retains authorized voice cloning.'
    report['fish-tts']=[{'field':'POST /fish/tts/request/references','kind':'omitted_optional_input','reason':'Coze requires nested audio and transcript for ordinary TTS.'}]
    (target/'fish-tts.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    (target/'fish-tts.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    doc=json.loads((ROOT/'plugins/localization.json').read_text())
    uri='/localization/translate'
    op=doc['paths'][uri]['post']
    body=op['requestBody']['content']['application/json']['schema']
    body.pop('oneOf',None)
    body['properties']['input']={'type':'string','description':'Markdown or plain text to translate.'}
    body['properties']['extension']['enum']=['md']
    body['properties']['extension']['default']='md'
    output=op['responses']['200']['content']['application/json']['schema']
    output['properties']['data']={'type':'string','description':'Translated Markdown or plain text.'}
    op['description']+=' This Coze form translates Markdown/plain text only; JSON-object translation is retained in the canonical API contract.'
    report['localization-md']=[{'field':'POST /localization/translate/request/input','kind':'representation','api_types':['object','string'],'coze_type':'string'}]
    (target/'localization-md.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    (target/'localization-md.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    doc=json.loads((target/'openai.json').read_text())
    canonical=json.loads((ROOT/'plugins/gpt-image.json').read_text())
    doc['info']=copy.deepcopy(canonical['info'])
    doc['paths']={uri:op for uri,op in doc['paths'].items() if uri in canonical['paths']}
    for uri in ('/openai/images/generations','/openai/images/edits'):
        body=doc['paths'][uri]['post']['requestBody']['content']['application/json']['schema']
        body['properties']['model']=copy.deepcopy(canonical['paths'][uri]['post']['requestBody']['content']['application/json']['schema']['properties']['model'])
    # Keep the explicit success contract for the Coze tool output editor.
    for methods in doc['paths'].values():
        for op in methods.values():
            op['responses']={'200':op['responses']['200']}
    doc=concrete_objects(doc)
    report['gpt-image']=[{'kind':'service_subset','reason':'Standalone GPT Image plugin uses only image generation, image editing and image task retrieval; existing OpenAI plugin is unchanged.'}]
    (target/'gpt-image.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    (target/'gpt-image.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))

    doc=json.loads((ROOT/'plugins/suno.json').read_text())
    # Re-importing the submitted scope must not re-enable failed, unverified or
    # destructive tools. The full API contract remains in plugins/suno.*.
    disabled_suno = {
        '/suno/mp4': {'post'},
        '/suno/custom-models': {'post'},
        '/suno/persona': {'post', 'delete'},
        '/suno/mashup-lyrics': {'post'},
        '/suno/projects': {'post'},
    }
    for uri, methods in disabled_suno.items():
        for method in methods:
            doc['paths'][uri].pop(method)
        if not doc['paths'][uri]:
            del doc['paths'][uri]
    notes.clear()
    for uri,methods in doc['paths'].items():
        for method,op in methods.items():
            loc=method.upper()+' '+uri
            for media in op.get('requestBody',{}).get('content',{}).values():
                media['schema']=project(media['schema'],loc+'/request')
            op['responses']={'200':op['responses']['200']}
            for media in op['responses']['200'].get('content',{}).values():
                media['schema']=project(media['schema'],loc+'/response')
    doc['paths']['/suno/midi']['post']['description']='Retrieve MIDI note data from supported audio. Submit once and poll getTaskResults. The completed response contains instruments and note events, not a downloadable MIDI file. If a generated audio ID is unsupported, upload audio you own and use the returned audio_id.'
    doc['paths']['/suno/timing']['post']['description']='Return aligned lyric words and their start/end times for supported audio. If a generated ID is unsupported, upload audio you own and use the returned audio_id. The store example is a short excerpt of a real 38-word response.'
    # Fresh Coze calls return objects for default lyrics and style expansion,
    # unlike the older array shapes in the public snapshot.
    lyrics=doc['paths']['/suno/lyrics']['post']
    lyrics['requestBody']['content']['application/json']['schema']['properties']['model'].update(enum=['default'],default='default')
    lyrics['responses']['200']['content']['application/json']['schema']['properties']['data']={
        'type':'object','properties':{'title':{'type':'string'},'text':{'type':'string'},
        'status':{'type':'string'},'tags':{'type':'array','items':{'type':'string'}}}}
    doc['paths']['/suno/style']['post']['responses']['200']['content']['application/json']['schema']['properties']['data']={
        'type':'object','properties':{'upsampled_tags':{'type':'string'}}}
    doc['paths']['/suno/upload']['post']['responses']['200']['content']['application/json']['schema']['properties']['data']={
        'type':'object','properties':{**{name:{'type':'string'} for name in
        ('audio_id','audio_url','image_url','image_large_url','title','lyric','style')},'duration':{'type':'number'}}}
    doc['paths']['/suno/timing']['post']['responses']['200']['content']['application/json']['schema']['properties']['data']={
        'type':'object','properties':{'aligned_words':{'type':'array','items':{'type':'object','properties':{
            'word':{'type':'string'},'start_s':{'type':'number'},'end_s':{'type':'number'},
            'p_align':{'type':'number'},'success':{'type':'boolean'}}}}}}
    vocal=doc['paths']['/suno/vox']['post']
    for name in ('async','callback_url'):
        vocal['requestBody']['content']['application/json']['schema']['properties'].pop(name,None)
    vocal['description']='Extract a vocal segment from an owned supported audio ID. This Coze tool waits for the vocal result; async mode is not exposed. Use the returned vocal_audio_url before it expires.'
    vocal['responses']['200']['content']['application/json']['schema']['properties']['data']={
        'type':'object','properties':{**{name:{'type':'string'} for name in
        ('id','source_clip_id','status','vocal_audio_url')},'vocal_start_s':{'type':'number'},'vocal_end_s':{'type':'number'}}}
    # Coze strips undeclared fields from task responses. Explicitly carry the
    # music result and export URLs for both a single task and a batch.
    music=copy.deepcopy(doc['paths']['/suno/audios']['post']['responses']['200']['content']['application/json']['schema']['properties'])
    music['data']['items']['properties']['file_url']={'type':'string','description':'Completed MP3 or WAV export URL.'}
    music['data']['items']['properties']['instruments']={'type':'array','items':{'type':'object','properties':{
        'program':{'type':'integer'},'notes':{'type':'array','items':{'type':'object','properties':{
            'pitch':{'type':'integer'},'start':{'type':'number'},'end':{'type':'number'},'velocity':{'type':'number'}}}}}}}
    music.update({
        'audio_url':{'type':'string'},'video_url':{'type':'string'},
        'cost':{'type':'object','properties':{'amount':{'type':'number'},'currency':{'type':'string'},'list_amount':{'type':'number'}}},
        'error':{'type':'object','properties':{'code':{'type':'string'},'message':{'type':'string'}}},
    })
    schema=doc['paths']['/suno/tasks']['post']['responses']['200']['content']['application/json']['schema']
    for props in (schema['properties'],schema['properties']['items']['items']['properties']):
        props['response']={'type':'object','properties':copy.deepcopy(music)}
    report['suno']=copy.deepcopy(notes)+[
        {'kind':'declared_output','reason':'Caller-owned HTTP authorization and explicit music result fields; native MCP OAuth remains a separate draft.'},
        {'kind':'submitted_scope','reason':'Only the 12 verified HTTP tools are imported. Five failed or unverified tools and unexercised persona deletion remain in the canonical API contract only.',
         'excluded_operations':[method.upper()+' '+uri for uri,methods in disabled_suno.items() for method in sorted(methods)]},
    ]
    doc=concrete_objects(doc)
    (target/'suno.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    (target/'suno.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))

    doc=json.loads((ROOT/'plugins/nano-banana.json').read_text())
    notes.clear()
    for uri,methods in doc['paths'].items():
        for method,op in methods.items():
            for media in op.get('requestBody',{}).get('content',{}).values():
                media['schema']=project(media['schema'],method.upper()+' '+uri+'/request')
            op['responses']={'200':op['responses']['200']}
            for media in op['responses']['200'].get('content',{}).values():
                media['schema']=project(media['schema'],method.upper()+' '+uri+'/response')
    doc=concrete_objects(doc)
    report['nano-banana']=copy.deepcopy(notes)+[{'kind':'prepared_full_form','reason':
        'Full two-tool reimport material; the earlier installed version and task-only projection have separate runtime evidence. This new file is not a store update.'}]
    (target/'nano-banana.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    (target/'nano-banana.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))

    # Prepared video store forms. These are not evidence of host import or a
    # successful generation; retain the caller's explicit model and task IDs.
    for key in ('seedance', 'happyhorse'):
        doc=json.loads((ROOT/'plugins'/f'{key}.json').read_text())
        notes.clear()
        for uri, methods in doc['paths'].items():
            for method, op in methods.items():
                for media in op.get('requestBody',{}).get('content',{}).values():
                    media['schema']=project(media['schema'],method.upper()+' '+uri+'/request')
                op['responses']={'200':op['responses']['200']}
                for media in op['responses']['200'].get('content',{}).values():
                    media['schema']=project(media['schema'],method.upper()+' '+uri+'/response')
        create=doc['paths'][f'/{key}/videos']['post']
        body=create['requestBody']['content']['application/json']['schema']
        body['properties'].pop('callback_url',None)
        if key=='seedance':
            body['properties'].pop('tools',None)
            body['properties']['content']['items']={
                'type':'object','required':['type','text'],'properties':{
                    'type':{'type':'string','enum':['text']},
                    'text':{'type':'string','maxLength':1000}}}
            create['description']+=' This prepared Coze form accepts text content only; image/audio/video references and web tools remain in the full API contract.'
            result={
                'type':'object','properties':{
                    'id':{'type':'string'},'task_id':{'type':'string'},
                    'status':{'type':'string'},'model':{'type':'string'},
                    'video_url':{'type':'string'},'duration':{'type':'number'},
                    'resolution':{'type':'string'},'ratio':{'type':'string'},
                    'content':{'type':'object','properties':{
                        'video_url':{'type':'string'},'last_frame_url':{'type':'string'}}}}}
        else:
            result=copy.deepcopy(create['responses']['200']['content']['application/json']['schema']['properties']['data'])
        response={'type':'object','properties':{
            'success':{'type':'boolean'},'task_id':{'type':'string'},
            'trace_id':{'type':'string'},'data':result,
            'error':{'type':'object','properties':{'code':{'type':'string'},'message':{'type':'string'}}}}}
        create['responses']['200']['content']['application/json']['schema']=copy.deepcopy(response)
        task=doc['paths'][f'/{key}/tasks']['post']['responses']['200']['content']['application/json']['schema']
        for props in (task['properties'],task['properties']['items']['items']['properties']):
            props['response']=copy.deepcopy(response)
        doc=concrete_objects(doc)
        report[key]=copy.deepcopy(notes)+[{'kind':'prepared_not_host_verified','reason':
            'Two-tool video form retains same-task retrieval and explicit media/error fields. No store submission or real Coze import is established; Seedance inputs are text-only in this projection.'}]
        (target/f'{key}.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
        (target/f'{key}.yaml').write_text(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False,width=100))
    (target/'compatibility-notes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Built',len(report),'Coze import projections; review representation differences before use.')

if __name__=='__main__':main()
