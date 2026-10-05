#!/usr/bin/env python3
"""Inventory matching MCP tools without invoking them or reading credentials."""
import argparse
import ast
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mcp-root',type=Path,required=True)
    parser.add_argument('--check-live',action='store_true')
    args=parser.parse_args()
    repo=args.mcp_root
    revision=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
    rows=json.loads((ROOT/'catalog/coverage.json').read_text())['services']
    services={}
    for row in rows:
        if row['service_type']!='Api':continue
        key=row['key'];directory={'nano-banana':'nanobanana'}.get(key,key);folder=repo/directory
        if not (folder/'tools').is_dir():
            services[key]={'mcp':None,'status':'no_dedicated_mcp','note':'No corresponding dedicated server exists in the MCP monorepo; the full public service contract remains the baseline.'}
            continue
        tools=[]
        for path in sorted((folder/'tools').rglob('*.py')):
            for fn in ast.walk(ast.parse(path.read_text())):
                if not isinstance(fn,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
                decorators=[d for d in fn.decorator_list if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr=='tool']
                if not decorators:continue
                name=next((k.value.value for d in decorators for k in d.keywords if k.arg=='name' and isinstance(k.value,ast.Constant)),fn.name)
                parameters=[{'name':a.arg,'annotation':ast.unparse(a.annotation) if a.annotation else None} for a in fn.args.args]
                defaults={a.arg:ast.unparse(v) for a,v in zip(fn.args.args[len(fn.args.args)-len(fn.args.defaults):],fn.args.defaults)}
                tools.append({'name':name,'description':ast.get_docstring(fn),'parameters':parameters,'defaults':defaults,'source':str(path.relative_to(repo)),'line':fn.lineno})
        endpoint=None;server_file=folder/'server.json'
        if server_file.exists():endpoint=json.loads(server_file.read_text()).get('remotes',[{}])[0].get('url')
        ingress=folder/'deploy/production/ingress.yaml'
        if not endpoint and ingress.exists():
            host=re.search(r'host:\s*([^\s]+)',ingress.read_text())
            if host:endpoint='https://'+host.group(1)+'/mcp'
        services[key]={'mcp':directory,'endpoint':endpoint,'mcp_tool_count':len(tools),'tools':tools,'coze_http_operation_count':row['tool_count'],'status':'native_mcp_target_not_connected' if endpoint else 'mcp_source_exists_hosted_transport_unverified','note':'MCP tools, API routes and Coze tools are separate inventories. A route count is not a parity claim.'}
    def fetch(item):
        key,service=item
        if not service.get('endpoint'):return key,None
        url=service['endpoint'].rsplit('/mcp',1)[0]+'/.well-known/mcp/server-card.json'
        result={}
        try:
            with urlopen(url,timeout=20) as response:card=json.load(response)
            result['public_card']={'url':url,'server_info':card.get('serverInfo'),'tool_names':[t['name'] for t in card.get('tools',[])],'source':'Public server card; not the authoritative live tools/list.'}
        except Exception as exc:result['public_card']={'url':url,'error':type(exc).__name__}
        # Service MCPs deliberately expose their public tool metadata to direct
        # clients. This marker is not an API credential and grants no API access.
        headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream','Authorization':'Bearer COZE_METADATA_ONLY_INVALID_TOKEN'}
        try:
            request=Request(service['endpoint'],headers=headers,data=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}}).encode())
            with urlopen(request,timeout=30) as response:payload=json.load(response)
            tools=payload.get('result',{}).get('tools',[])
            result['live_tools']={'tool_count':len(tools),'tools':tools,'next_cursor':payload.get('result',{}).get('nextCursor'),'source':'Live tools/list with a public invalid discovery marker; no effective service credential or tools/call.'}
            if not tools:result['live_tools']['error']=payload.get('error','Empty tool list')
        except Exception as exc:result['live_tools']={'error':type(exc).__name__}
        return key,result
    if args.check_live:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for key,evidence in pool.map(fetch,services.items()):
                if not evidence:continue
                service=services[key];service['live_public_card']=evidence['public_card'];service['live_tools']=evidence['live_tools']
                if evidence['live_tools'].get('tools'):
                    service['source_mcp_tool_count']=service['mcp_tool_count'];service['source_tools']=service['tools']
                    service['tools']=[{'name':t['name'],'description':t.get('description',''),'input_schema':t.get('inputSchema',{}),'annotations':t.get('annotations',{})} for t in evidence['live_tools']['tools']]
                    service['mcp_tool_count']=len(service['tools']);service['benchmark_source']='live tools/list'
    output={'source_repository':'AceDataCloud/MCPs','source_revision':revision,'snapshot_date':'2026-10-05','benchmark':'One service plugin should match its MCP business capabilities, including generation, editing, retrieval, management and information tools. Names/counts alone are not parity.','exclusions':['Datasets are excluded by user instruction.','Retired Sora and MCP-only services without a current public catalog entry are not promoted.'],'services':services}
    (ROOT/'catalog/mcp-parity.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(f"Inventoried {sum(bool(s['mcp']) for s in services.values())} matching MCPs for {len(services)} API services.")
    print(f"Suno target: {services['suno']['mcp_tool_count']} MCP tools (live when requested); {services['suno']['coze_http_operation_count']} HTTP operations is a separate count.")


if __name__=='__main__':main()
