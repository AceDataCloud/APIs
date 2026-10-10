#!/usr/bin/env python3
"""Build review/import assets from a dated, anonymous public catalog snapshot.

No network requests, credentials, paid runs or Coze publishing are performed.
"""
from __future__ import annotations
import ast
import copy
import hashlib
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
HTTP = {'get', 'post', 'put', 'patch', 'delete'}
SLUGS = {'b1fbcc32-e218-4253-9dc3-4fe600a1bfb9':'aichat', 'a0a76008-85ff-4c46-8db7-76481721b9fb':'identity', '349bfa75-d270-44e9-8188-9894e3b9512c':'shorturl','bd4eaf26-4efe-4904-a045-8b83ed56f885':'localization'}
AUTH = 'Bind your own Ace Data Cloud credential privately as Bearer YOUR_API_TOKEN in Authorization. Usage is billed to your account. Never place a token in chat or shared examples.'
SETUP = 'https://platform.acedata.cloud/?from=coze'
IDS = {'seedream','flux','serp','shorturl'}
OMIT_PATHS = {'/v1/live/sessions':'Requires a live session transport; not a conventional JSON tool.', '/v1/audio/speech':'Binary audio response needs a media URL adapter for Coze.', '/v1/audio/transcriptions':'Multipart file upload needs a tested Coze file adapter.'}
DEFAULTS = {'/seedream/images':{'model':'doubao-seedream-5-0-lite-260128','size':'2K'}, '/flux/images':{'model':'flux-2-pro','size':'1:1','action':'generate','count':1}, '/serp/google':{'type':'search','number':3}, '/nano-banana/images':{'model':'nano-banana-2','action':'generate'}, '/veo/videos':{'model':'veo31-fast','action':'text2video'}, '/kling/videos':{'model':'kling-v2-6','action':'text2video'}, '/producer/audios':{'model':'FUZZ-2.0','action':'generate'}, '/wan/videos':{'model':'wan2.6-t2v'}, '/suno/lyrics':{'model':'default'}, '/openai/images/generations':{'model':'gpt-image-1'}, '/openai/images/edits':{'model':'gpt-image-1'}, '/openai/embeddings':{'model':'text-embedding-3-small'}}
IMAGE_TASK_FIELDS = {
    'success':{'type':'boolean'},
    'task_id':{'type':'string'},
    'trace_id':{'type':'string'},
    'data':{'type':'array','items':{'type':'object','properties':{
        'image_url':{'type':'string'},'prompt':{'type':'string'},
    }}},
    'cost':{'type':'object','properties':{
        'amount':{'type':'number'},'list_amount':{'type':'number'},'currency':{'type':'string'},
    }},
}
VIDEO_TASK_FIELDS = {
    'success':{'type':'boolean'},
    'task_id':{'type':'string'},
    'trace_id':{'type':'string'},
    'data':{'type':'array','items':{'type':'object','properties':{
        'id':{'type':'string'},'video_url':{'type':'string'},
        'state':{'type':'string'},'duration':{'type':'number'},
        'aspect_ratio':{'type':'string'},'prompt':{'type':'string'},
    }}},
    'cost':{'type':'object','properties':{
        'amount':{'type':'number'},'list_amount':{'type':'number'},'currency':{'type':'string'},
    }},
    'error':{'type':'object','properties':{
        'code':{'type':'string'},'message':{'type':'string'},
    }},
}
OPENAI_IMAGE_TASK_FIELDS = {
    **copy.deepcopy(IMAGE_TASK_FIELDS),
    'model':{'type':'string'},
    'created':{'type':'number'},
    'data':{'type':'array','items':{'type':'object','properties':{
        'url':{'type':'string'},'b64_json':{'type':'string'},
        'revised_prompt':{'type':'string'},
    }}},
    'error':copy.deepcopy(VIDEO_TASK_FIELDS['error']),
}
FISH_VOICE_FIELDS = {
    '_id':{'type':'string'},'title':{'type':'string'},
    'description':{'type':'string'},'state':{'type':'string'},
    'type':{'type':'string'},'visibility':{'type':'string'},
    'licensed':{'type':'boolean'},
    'languages':{'type':'array','items':{'type':'string'}},
    'tags':{'type':'array','items':{'type':'string'}},
}
TASK_RESPONSE_FIELDS = {
    '/nano-banana/tasks':IMAGE_TASK_FIELDS,
    '/qwen-image/tasks':IMAGE_TASK_FIELDS,
    '/grok/tasks':VIDEO_TASK_FIELDS,
    '/gemini/tasks':VIDEO_TASK_FIELDS,
    '/openai/tasks':OPENAI_IMAGE_TASK_FIELDS,
}


def slug(s):
    return SLUGS.get(s['id'],(s['alias'] or '').lower())


def pointer(doc, ref):
    if not ref.startswith('#/'):
        raise ValueError('External reference cannot be imported: '+ref)
    cur=doc
    for part in ref[2:].split('/'):
        cur=cur[part.replace('~1','/').replace('~0','~')]
    return cur


def resolve(value, doc, stack=()):
    if isinstance(value,list): return [resolve(v,doc,stack) for v in value]
    if not isinstance(value,dict): return value
    if '$ref' in value:
        ref=value['$ref']
        if ref in stack: raise ValueError('Recursive schema requires an adapter: '+ref)
        base=copy.deepcopy(pointer(doc,ref));base.update({k:v for k,v in value.items() if k!='$ref'})
        return resolve(base,doc,stack+(ref,))
    result={k:resolve(v,doc,stack) for k,v in value.items() if k not in ['$schema','examples','example','prefixItems'] and not (k == 'rank' and isinstance(v,(int,float)))}
    if isinstance(result.get('description'),str) and result['description'].startswith("{'zh-cn':"):
        try:result['description']=ast.literal_eval(result['description']).get('en',result['description'])
        except (ValueError,SyntaxError):pass
    # Many public error variants differ only by examples. After examples are
    # removed, keep a single equivalent branch so oneOf still accepts errors.
    for kind in ['oneOf','anyOf']:
        if kind in result:
            unique={json.dumps(v,sort_keys=True,ensure_ascii=False):v for v in result[kind]}
            result[kind]=list(unique.values())
    if 'const' in result: result['enum']=[result.pop('const')]
    if isinstance(result.get('type'),list):
        kinds=result['type'];result['nullable']='null' in kinds;result['type']=next(k for k in kinds if k!='null')
    # OAS 3.1 exclusive bounds are numbers; 3.0 uses the bound + a boolean.
    for bound in ['Minimum','Maximum']:
        key='exclusive'+bound
        if type(result.get(key)) in (int,float):
            result[bound.lower()]=result[key];result[key]=True
    return result


def import_body(schema):
    """Expose union fields to the importer while preserving branch constraints."""
    s=copy.deepcopy(schema)
    variants=s.get('oneOf',s.get('anyOf',[]))
    if variants and all(v.get('type')=='object' or 'properties' in v for v in variants):
        props=copy.deepcopy(s.get('properties',{}));req=None
        for v in variants:
            vr=set(v.get('required',[]));req=vr if req is None else req&vr
            for k,p in v.get('properties',{}).items():
                if k not in props:props[k]=copy.deepcopy(p)
                elif props[k]!=p:
                    if props[k].get('type')==p.get('type') and props[k].get('enum') and p.get('enum'):
                        props[k]['enum']=list(dict.fromkeys(props[k]['enum']+p['enum']))
                    else:
                        props[k]={'anyOf':[props[k],copy.deepcopy(p)]}
        s['type']='object';s['properties']=props
        req=set(s.get('required',[])) | (req or set())
        if req:s['required']=sorted(req)
    return s


def sample(schema,name=''):
    if 'default' in schema:return schema['default']
    if 'enum' in schema:return schema['enum'][0]
    if 'example' in schema and name not in ['name','phone','mobile','id_card','bank_card','image','image_url','audio_url','video_url','website_url','website_key','references','voices']:return schema['example']
    if 'oneOf' in schema or 'anyOf' in schema:
        return sample((schema.get('oneOf') or schema.get('anyOf'))[0],name)
    kind=schema.get('type')
    if kind=='object':return {k:sample(schema.get('properties',{}).get(k,{}),k) for k in schema.get('required',[])}
    if kind=='array':return [sample(schema.get('items',{}),name)]
    if kind=='boolean':return False
    if kind in ['integer','number']:return schema.get('minimum',1)
    if name in ['id','task_id','audio_id','video_id','persona_id','version_id']:return 'REPLACE_WITH_OWNED_'+name.upper()
    if name in ['prompt','question','text','input']:return 'A calm sunrise over a mountain lake.'
    if name=='messages':return [{'role':'user','content':'Explain why the sky appears blue in two sentences.'}]
    if name in ['name','phone','mobile','id_card','bank_card','website_key']:return 'AUTHORIZED_TEST_FIXTURE_REQUIRED'
    if name.endswith('_url') or name in ['url','image']:return 'https://example.com/authorized-test-input'
    if name=='model':return 'SELECT_A_DOCUMENTED_MODEL'
    return 'REPLACE_'+name.upper()


def tool_name(path, method):
    exact={
        '/v1/messages/count_tokens':'countTokens','/v1/messages':'createMessage',
        '/v1beta/models/{model}:generateContent':'generateContent',
        '/aichat/conversations':'createConversation','/aichat2/conversations':'manageConversation',
        '/serp/google':'searchGoogle','/shorturl':'createShortLink',
        '/openai/images/generations':'generateImage','/openai/images/edits':'editImage',
        '/openai/embeddings':'createEmbeddings','/openai/responses':'createResponse',
        '/webextrator/render':'renderPage','/webextrator/extract':'extractPage',
        '/localization/translate':'translateContent','/fish/tts':'textToSpeech',
        '/fish/model/{id}':'getVoice','/suno/voices':'cloneVoice',
        '/suno/custom-models':'manageMusicModel','/suno/projects':'manageMusicProject',
        '/suno/mashup-lyrics':'blendLyrics','/suno/style':'refineMusicStyle',
        '/suno/vox':'extractVocalStem','/suno/timing':'getLyricTiming',
        '/suno/mp3':'exportMp3','/suno/mp4':'exportMusicVideo','/suno/midi':'exportMidi',
        '/producer/videos':'createMusicVideo',
        '/kling/talking-photo':'createTalkingPhoto','/kling/motion':'controlVideoMotion',
        '/kling/lip-sync':'syncVideoLips','/kling/goods-studio':'createProductMedia',
        '/kling/video-commerce':'createCommerceVideo',
        '/captcha/tasks':'getChallengeResult','/captcha/recognition/image2text':'recognizeCaptchaText',
        '/captcha/token/turnstile':'getTurnstileToken','/captcha/token/recaptcha2':'getRecaptchaV2Token',
        '/captcha/token/recaptcha3':'getRecaptchaV3Token','/captcha/recognition/recaptcha2':'recognizeRecaptchaV2',
        '/captcha/token/hcaptcha':'getHcaptchaToken','/captcha/recognition/hcaptcha':'recognizeHcaptcha',
        '/identity/idcard/ocr':'recognizeIdCard'}
    if path in exact:return exact[path]
    if path=='/fish/model':return {'get':'listVoices','post':'createVoice','delete':'deleteVoice'}[method]
    if path=='/suno/persona':return {'get':'listPersonas','post':'createPersona','delete':'deletePersona'}[method]
    for suffix,name in [('/chat/completions','chatCompletion'),('/tasks','getTaskResults'),('/videos','generateVideo'),('/images','generateImage'),('/audios','generateMusic'),('/lyrics','generateLyrics'),('/upload','uploadAudio'),('/wav','exportWav'),('/voices','createVoice')]:
        if path.endswith(suffix):return name
    match=re.fullmatch(r'/identity/(idcard|bankcard|phone)/check-([1-4])e',path)
    if match:return 'verify'+{'idcard':'IdCard','bankcard':'BankCard','phone':'Phone'}[match[1]]+match[2]+'e'
    raise ValueError('A user-facing tool name is required: '+method+' '+path)


def build_operation(a,path,method,source):
    d=a['definition'];op=resolve(source,d)
    op.pop('security',None);op.pop('callbacks',None);op.pop('tags',None)
    op['operationId']=tool_name(path,method)
    if method=='post' and path in {'/seedream/images','/flux/images','/serp/google','/shorturl'}:
        op['operationId']={'/seedream/images':'generateImage','/flux/images':'generateImage','/serp/google':'searchGoogle','/shorturl':'createShortLink'}[path]
    op['summary']=(op.get('summary') or a['path']).split('\n')[0][:160]
    detail=(op.get('description') or op['summary']).strip()
    op['description']=detail[:1000]+' Full input requirements: '+a['document_url']
    if path=='/maestro/tasks':
        op['description']+=' Maestro completion is status=succeeded with response.success=true and response.data.variants[].output_url.'
    if path=='/minimax/tasks':
        op['description']+=' MiniMax completion is task.status=succeeded with a non-empty task.content.url. Its result does not use the generic response wrapper.'
    if path.endswith('/tasks'):
        op['description']+=' A non-null response can be a progress snapshot. Require terminal success and a non-empty primary media URL or content, not just a cover image or an empty data array.'
    op['externalDocs']={'url':a['document_url']}
    pars=op.setdefault('parameters',[])
    pars[:]=[x for x in pars if x.get('name','').lower() not in ['authorization','x-api-key']]
    pars.append({'name':'Authorization','in':'header','required':True,'description':AUTH,'schema':{'type':'string'}})
    rb=op.get('requestBody',{});content=rb.get('content',{})
    if 'application/json' in content:
        content={'application/json':content['application/json']};rb['content']=content
        body=content['application/json'];body.pop('example',None);body.pop('required',None)
        s=import_body(body.get('schema',{}));body['schema']=s
        props=s.get('properties',{})
        for k,v in DEFAULTS.get(path,{}).items():
            if k in props:props[k]['default']=v
        if 'stream' in props:props['stream'].update(default=False,enum=[False],description='Use false for Coze JSON tool results.')
        if path=='/seedream/images' and 'stream' in props:
            props['stream'].pop('default',None)
            props['stream']['description']='Omit this field for Seedream Pro. Streaming is unavailable in this JSON-only plugin.'
        if path=='/flux/images':
            props['size']['description']='Flux 2 uses an aspect ratio such as 1:1 or 16:9. Pixel-size strings such as 1024x1024 fail for Flux 2. Check model-specific requirements before changing the model.'
        if 'async' in props:
            props['async']['default']=True
            op['description']+=' Submit once with async=true. Retain task_id and poll the matching task tool; a task ID is not a completed result. Do not resubmit while pending.'
        # Callback delivery is optional; polling has no public receiver to configure.
        if 'callback_url' in props:props['callback_url'].pop('default',None)
        if path.endswith('/tasks') and 'action' in props and props['action'].get('enum'):
            props['action']['enum']=[v for v in props['action']['enum'] if v!='delete']
        if path=='/aichat2/conversations' and 'action' in props:
            props['action']['default']='chat'
        # OAS examples remain reference fixtures, never claimed to be real Coze runs.
    op['responses']={k:v for k,v in op.get('responses',{}).items() if k in ['200','201','202','400','401','403','429','500','default']}
    for status,resp in op['responses'].items():
        for c in resp.get('content',{}).values():
            c.pop('example',None);c.pop('properties',None);c.pop('required',None)
            if 'schema' in c:c['schema']=import_body(c['schema'])
            if path=='/fish/tts' and 'schema' in c and status=='200':
                # The async acknowledgement has task_id/started_at rather
                # than the audio_url in the completed synchronous response.
                c['schema'].setdefault('properties',{}).update({
                    'task_id':{'type':'string'},'started_at':{'type':'number'},
                    'trace_id':{'type':'string'},
                })
            if path=='/webextrator/tasks' and 'schema' in c:
                schema=c['schema']
                # import_body has already merged the response union into
                # properties. Keeping oneOf makes Coze display duplicate
                # output rows, so use that merged shape for this tool.
                schema.pop('oneOf',None)
                content_fields={
                    'kind':{'type':'string'},'url':{'type':'string'},
                    'finalUrl':{'type':'string'},'title':{'type':'string'},
                    'markdown':{'type':'string'},'text':{'type':'string'},
                    'success':{'type':'boolean'},
                    'error':{'type':'object','properties':{'code':{'type':'string'},'message':{'type':'string'}}},
                }
                # The public response is dynamic. Coze drops its content
                # unless fields are declared for both retrieve and batch.
                for container in (schema.get('properties',{}),
                                  schema.get('properties',{}).get('items',{}).get('items',{}).get('properties',{})):
                    response=container.get('response')
                    if response and response.get('type')=='object':
                        response['properties']=content_fields
            if path=='/fish/model' and method.lower()=='get' and status=='200' and 'schema' in c:
                props=c['schema'].setdefault('properties',{})
                props['items']['items']['properties']=copy.deepcopy(FISH_VOICE_FIELDS)
                props.update({
                    'max_offset':{'type':'number'},
                    'accessible_upper_bound':{'type':'number'},
                    'window_limited':{'type':'boolean'},
                    'total_is_exact':{'type':'boolean'},
                    'has_more':{'type':'boolean'},
                })
            if path in TASK_RESPONSE_FIELDS and 'schema' in c:
                schema=c['schema']
                schema.pop('oneOf',None)
                for container in (schema.get('properties',{}),
                                  schema.get('properties',{}).get('items',{}).get('items',{}).get('properties',{})):
                    response=container.get('response')
                    if response and response.get('type')=='object':
                        response['properties']=copy.deepcopy(TASK_RESPONSE_FIELDS[path])
    return op


def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def main():
    src=json.loads((ROOT/'catalog/public-snapshot.json').read_text());profiles=json.loads((ROOT/'catalog/profiles.json').read_text());contracts=src['contracts'];coverage=[];listings={};cases=[]
    scope=json.loads((ROOT/'catalog/launch-scope.json').read_text())
    for s in src['services']:
        if s['type'] in scope['excluded_types'] or slug(s) in scope['excluded_service_keys']:continue
        key=slug(s);row={'key':key,'service_id':s['id'],'service_type':s['type'],'title':s['title'],'description':s['description'],'source_url':f"https://platform.acedata.cloud/services/{s['id']}",'icon':f'icons/{key}.png','operations':[],'blockers':[]}
        if s['type']!='Api':
            row['delivery']='catalog_assistant';row['name']=s['title'];row['brief']=s['description'];row['readiness']='guide_prepared'
            row['blockers']=['Requires a user-owned deployment URL and scoped authentication before functional plugin creation.'] if s['type']=='Deployment' else (['A local developer client; provided through setup guidance rather than a hosted Coze tool.'] if s['type']=='Agent' else ['Catalog and acquisition guidance only; no public query API is declared.'])
            for o in s['operations']:row['operations'].append({**o,'disposition':'guide_only'})
            coverage.append(row);continue
        p=profiles[key];start_url=row['source_url']+'?from=coze'
        if key=='deepseek':start_url='https://platform.acedata.cloud/services/b1fbcc32-e218-4253-9dc3-4fe600a1bfb9?from=coze'
        row.update({k:p[k] for k in ['name','brief','group','description','scenarios']});row['delivery']='http_plugin'
        spec={'openapi':'3.0.1','info':{'title':p['name'],'version':'2.0.0','description':p['description']+' '+AUTH+' Start: '+start_url},'servers':[{'url':'https://api.acedata.cloud'}],'paths':{}}
        for meta in s['operations']:
            a=contracts.get(meta['api_id'])
            if not a:
                row['operations'].append({**meta,'disposition':'excluded','reason':'No current public API document and import contract.'});continue
            for path,value in a['definition'].get('paths',{}).items():
                for method,source in value.items():
                    if method not in HTTP:continue
                    item={'api_id':a['id'],'path':path,'method':method.upper(),'stage':a['stage'],'docs':a['document_url']}
                    reason=OMIT_PATHS.get(path)
                    if 'streamGenerateContent' in path:reason='Streaming transport; use generateContent with a JSON response.'
                    # Management definitions are included; deletion is never exercised by the draft builder.
                    if reason:row['operations'].append({**item,'disposition':'adapter_or_console','reason':reason});continue
                    try:op=build_operation(a,path,method,source)
                    except (ValueError,KeyError) as e:
                        row['operations'].append({**item,'disposition':'adapter_required','reason':str(e)});continue
                    spec['paths'].setdefault(path,{})[method]=op
                    row['operations'].append({**item,'operation_id':op['operationId'],'disposition':'schema_prepared'})
                    schema=op.get('requestBody',{}).get('content',{}).get('application/json',{}).get('schema',{})
                    ex=sample(schema)
                    if isinstance(ex,dict):
                        for k in ['model','action','async','stream']:
                            pr=schema.get('properties',{}).get(k)
                            if pr and ('default' in pr or k=='model'):ex[k]=sample(pr,k)
                        if path.endswith('/chat/completions'):ex['messages']=[{'role':'user','content':'Explain why the sky appears blue in two sentences.'}]
                        if path=='/shorturl':ex={'content':'https://platform.acedata.cloud/?from=coze'}
                        if path=='/serp/google':ex={'query':'Ace Data Cloud API documentation','type':'search','number':3}
                    case={'service':key,'api_id':a['id'],'operation_id':op['operationId'],'method':method.upper(),'path':path,'request':{'headers':{'Authorization':'Bearer YOUR_API_TOKEN'},'body':ex if method!='get' else None},'status':'not_run','fixture_kind':'draft_request_not_execution_evidence','acceptance':['Validate the request against the current model/action requirements.','Confirm a successful real response and expected result fields.','For async creation, poll the matching retrieval tool to a terminal result.','Inspect the returned media or content and reconcile billed Credits.'],'special_authorization':method=='delete' or key in ['identity','turnstile','recaptcha','hcaptcha','image2text'] or any(w in path for w in ['voices','custom-models'])}
                    cases.append(case)
        # DeepSeek models are explicitly published on the shared AI Dialogue API.
        # Keep the hidden brand-specific contract excluded; expose only this
        # documented model subset, with the route visible in coverage and copy.
        if key=='deepseek':
            a=contracts['1d58971c-e3cd-4713-a3ce-854a731adb14'];path='/aichat/conversations'
            op=build_operation(a,path,'post',a['definition']['paths'][path]['post'])
            model=op['requestBody']['content']['application/json']['schema']['properties']['model']
            model['enum']=[v for v in model['enum'] if v.startswith('deepseek-')]
            model['default']='deepseek-v4-flash'
            op['summary']='Ask a DeepSeek model through AI Dialogue'
            op['description']='Use the public AI Dialogue conversation API with an explicitly selected DeepSeek model. '+a['document_url']
            spec['paths'][path]={'post':op}
            row['operations'].append({'api_id':a['id'],'path':path,'method':'POST','operation_id':op['operationId'],'disposition':'schema_prepared','docs':a['document_url'],'reason':'Published AI Dialogue model subset; the hidden brand-specific API is excluded.'})
            row['blockers'].append('Uses the published AI Dialogue conversation API; verify this exact model and route before launch.')
        # All captcha services share the public task retrieval API.
        if key in ['turnstile','image2text','recaptcha']:
            a=contracts['0c6538fd-de94-4e7c-b876-b45ded6487bb'];path='/captcha/tasks';op=build_operation(a,path,'post',a['definition']['paths'][path]['post']);spec['paths'][path]={'post':op};row['operations'].append({'api_id':a['id'],'path':path,'method':'POST','operation_id':op['operationId'],'disposition':'schema_prepared','reason':'Shared public CAPTCHA task retrieval.'})
        row['tool_count']=sum(len(v) for v in spec['paths'].values());row['readiness']='draft_assets_prepared' if row['tool_count'] else 'blocked_public_contract'
        row['plugin_url']=None
        row['coze_state']='existing_draft_needs_full_update' if key in IDS else 'not_created'
        if key=='flux':row['coze_state']='workspace_v1_published_before_review_hold_store_not_submitted'
        row['validation']='partial_real_trial' if key in IDS else 'not_run'
        row['blockers']+=['Expanded tool set requires Coze import verification and authorized real trials.']
        if key in ['identity','turnstile','recaptcha','hcaptcha','image2text']:row['blockers'].append('Controlled authorized fixtures and a service-specific privacy review are required for real tests.')

        row['schema']=f'plugins/{key}.yaml' if spec['paths'] else None
        if spec['paths']:
            (ROOT/'plugins'/f'{key}.yaml').write_text(yaml.safe_dump(spec,allow_unicode=True,sort_keys=False,width=100))
            write_json(ROOT/'plugins'/f'{key}.json',spec)
            if key in {'suno','seedream','flux','serp','shorturl','kling','veo','seedance'}:
                (ROOT/f'{key}.yaml').write_text(yaml.safe_dump(spec,allow_unicode=True,sort_keys=False,width=100))
            if key=='openai':
                (ROOT/'image.yaml').write_text(yaml.safe_dump(spec,allow_unicode=True,sort_keys=False,width=100))
        listing={k:row[k] for k in ['name','brief','description','scenarios','icon']}
        listing['category']={'Chat':'Productivity','Video':'Video','Image':'Photography','Multimodal':'Productivity','Music':'Music','Audio':'Music','Search':'Web Search','Utility':'Tools','Avatar':'Video','Verification':'Tools'}[p['group']]
        listing['about']=p['description']+'\n\n'+AUTH+'\nGet started: '+start_url
        if key=='deepseek':listing['about']+=' Use a Global credential or one authorized for the AI Dialogue API.'
        listing['privacy_review']={'data_sent':'User-selected prompts, content, URLs and request parameters; Authorization carries the caller credential.','recipient':'Ace Data Cloud API','retention':'Verify current published privacy terms; no retention promise is made in this draft.','sensitive_inputs':key in ['identity','digitalhuman','dreamina','fish','suno']}
        listings[key]=listing;coverage.append(row)
    covered={(c['service'],c['operation_id']) for c in cases}
    for row in coverage:
        if not row.get('schema'):continue
        definition=json.loads((ROOT/'plugins'/f"{row['key']}.json").read_text())
        for item in row['operations']:
            if item['disposition']!='schema_prepared' or (row['key'],item['operation_id']) in covered:continue
            op=definition['paths'][item['path']][item['method'].lower()]
            body=op.get('requestBody',{}).get('content',{}).get('application/json',{}).get('schema',{})
            cases.append({'service':row['key'],'api_id':item['api_id'],'operation_id':item['operation_id'],'method':item['method'],'path':item['path'],'request':{'headers':{'Authorization':'Bearer YOUR_API_TOKEN'},'body':sample(body)},'status':'not_run','fixture_kind':'draft_request_not_execution_evidence','acceptance':['Validate required inputs. Use an authorized owned task or controlled fixture. Inspect the real output and billed Credits.'],'special_authorization':row['key'] in ['turnstile','image2text','recaptcha']})
    guide=['Ace Data Cloud public service guide','Catalog date: '+src['retrieved_at'],'This is catalog guidance, not proof of Coze store publication.']
    for row in coverage:
        guide+=['','SERVICE: '+row['title'],'TYPE: '+row['service_type'],'DESCRIPTION: '+row['description'],'URL: '+row['source_url'],'COZE ENTRY: '+row['delivery']]
        if row['service_type']=='Dataset':guide+=['NEXT STEP: Open the service page to review acquisition, access and licensing requirements. No public query API is declared.']
        elif row['service_type']=='Deployment':guide+=['NEXT STEP: Provision a user-owned deployment and configure its own URL and access before automation. Sending messages is not enabled by this guide.']
        elif row['service_type']=='Agent':guide+=['NEXT STEP: Follow the corresponding developer client setup guide; the client runs in the user environment.']
        else:guide+=['NEXT STEP: Select the matching plugin once it is published, then privately configure your own Ace Data Cloud credential.']
    (ROOT/'catalog/service-guide.txt').write_text('\n'.join(guide)+'\n')
    write_json(ROOT/'catalog/coverage.json',{'snapshot_date':src['retrieved_at'],'services':coverage})
    write_json(ROOT/'listings.json',listings)
    write_json(ROOT/'examples/catalog/validation-cases.json',cases)
    print(f'{len(coverage)} services, {len(listings)} API listings, {sum(1 for x in coverage if x.get("schema"))} schemas, {sum(x.get("tool_count",0) for x in coverage)} tools, {len(cases)} draft test cases')

if __name__=='__main__':main()
