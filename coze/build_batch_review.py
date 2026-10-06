#!/usr/bin/env python3
"""Build a focused review for Coze drafts with a verified core tool call."""

import argparse
import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# The evidence proves these particular calls, not all tools in a plugin.
CASES = [
    ("suno", "原生 MCP 生成歌曲、查询任务，取得两条可访问的 MP3", ["e2e-v4/suno-submission-coze-ax.txt", "e2e-v4/suno-poll-coze-ax.txt", "e2e-v4/suno-media-probe.json"], "其余 MCP 工具和用户 OAuth 待验。"),
    ("deepseek", "文本对话返回有效回复", ["e2e-v4/deepseek-coze-result.txt"], "仅验证文本对话。"),
    ("shorturl", "创建短链接并返回可用 URL", ["e2e-v5/shorturl-coze-result.txt"], "其他 MCP 能力待验。"),
    ("serp", "Google 搜索返回结构化结果链接", ["e2e-v5/google-search-coze-result.txt"], "其他搜索类型与 MCP 工具待验。"),
    ("webextrator", "提取网页并在 Coze 读回标题、正文和 Markdown", ["e2e-v5/webextractor-submit-coze.txt", "e2e-v6/webextractor-coze-result.txt"], "其他提取模式与 MCP 工具待验。"),
    ("claude", "文本对话返回有效回复", ["e2e-v6/claude-coze-chat-pass.txt"], "多模态和其余接口待验。"),
    ("openai", "文本对话返回有效回复", ["e2e-v6/openai-coze-chat-pass.txt"], "多模态、工具调用和其余接口待验。"),
    ("kimi", "文本对话返回有效回复", ["e2e-v6/kimi-coze-chat-pass.txt"], "其余输入类型待验。"),
    ("gemini", "文本对话返回有效回复", ["e2e-v6/gemini-coze-chat-pass.txt"], "多模态和其余接口待验。"),
    ("grok", "文本对话返回有效回复", ["e2e-v6/grok-coze-chat-pass.txt"], "其余接口与 MCP 工具待验。"),
    ("glm", "文本对话返回有效回复", ["e2e-v6/glm-coze-chat-pass.txt"], "其余模型和 MCP 工具待验。"),
    ("nano-banana", "提交图像任务，Coze 读回成品 JPEG，链接返回 200", ["e2e-v6/nano-banana-submit.txt", "e2e-v6/nano-banana-coze-task-pass.txt"], "编辑等其他 MCP 能力待验。"),
    ("qwen-image", "提交图像任务，Coze 读回成品 PNG，链接返回 200", ["e2e-v6/qwen-image-submit.txt", "e2e-v6/qwen-image-coze-task-pass.txt"], "编辑等其他能力待验。"),
    ("fish", "提交语音任务，Coze 读回成品 MP3，链接返回 200", ["e2e-v6/fish-submit-coze.txt", "e2e-v6/fish-coze-task-pass.txt"], "音色管理与其余 MCP 能力待验。"),
    ("localization", "Markdown 文本翻译得到中文结果", ["e2e-v6/localization-md-coze-pass.txt"], "仅 Markdown 模式通过；JSON 对象输入仍失败。"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    evidence_root = args.evidence_root.resolve()
    output = args.output.resolve()
    drafts = json.loads((evidence_root / "coze-drafts.json").read_text())
    gate = json.loads((evidence_root / "e2e-v4/launch-gate.json").read_text())
    gates = {row["key"]: row for row in gate["services"]}
    coverage = {row["key"]: row for row in json.loads((ROOT / "catalog/coverage.json").read_text())["services"]}
    listings = json.loads((ROOT / "listings.json").read_text())
    parity = json.loads((ROOT / "catalog/mcp-parity.json").read_text())["services"]
    native = json.loads((evidence_root / "suno-native-mcp-draft.json").read_text())
    entries = []
    for key, proof, files, caveat in CASES:
        state = gates[key]["coze_real_call"]
        if state != "pass":
            raise ValueError(f"{key}: expected a verified Coze call, got {state}")
        row = coverage[key]
        draft = drafts[key]
        if row["service_type"] != "Api" or draft.get("launch_excluded") or draft.get("name") != row["name"]:
            raise ValueError(f"{key}: launch scope or Coze draft metadata mismatch")
        if draft.get("state") != "unpublished":
            raise ValueError(f"{key}: unexpected publication state")
        for file in files:
            if not (evidence_root / file).is_file():
                raise FileNotFoundError(file)
        entries.append({
            "key": key,
            "name": row["name"],
            "group": row["group"],
            "brief": row["brief"],
            "icon": "data:image/png;base64," + base64.b64encode((ROOT / row["icon"]).read_bytes()).decode(),
            "about": listings[key]["about"],
            "scenarios": listings[key]["scenarios"],
            "draft_url": draft["url"],
            "native_url": native["url"] if key == "suno" else None,
            "tool_count": draft["tool_count"],
            "mcp_tool_count": parity[key].get("mcp_tool_count"),
            "proof": proof,
            "evidence": files,
            "caveat": caveat,
            "partial": key == "localization",
        })
    if len(entries) != 15 or gate["coze_real_call_passed"] != 15:
        raise ValueError("Batch count and launch gate disagree")
    payload = json.dumps({"entries": entries, "credits": gate["credits_used_total"], "cap": gate["budget_credit_cap"]}, ensure_ascii=False).replace("</", "<\\/")
    html = r'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Coze 第一批插件审查 · 15 款</title>
<style>
:root{--ink:#1a2940;--muted:#60728a;--line:#dbe3ed;--blue:#155fbd;--green:#166a51;--gold:#9b6612;--bg:#f4f7fb}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;color:var(--ink);background:var(--bg);line-height:1.55}a{color:var(--blue)}button,input,select,textarea{font:inherit}.wrap{max-width:1240px;margin:auto;padding:0 28px}.hero{background:#102b48;color:white;padding:34px 0 30px}.eyebrow{font-size:12px;letter-spacing:.18em;color:#82c7dc;font-weight:700}h1{font-size:36px;line-height:1.2;margin:11px 0 9px}.hero p{margin:0;color:#d0e0ee;max-width:830px}.numbers{display:flex;gap:36px;margin-top:23px}.number{border-top:1px solid #56708b;min-width:125px;padding-top:8px}.number strong{display:block;font-size:26px}.number span{display:block;font-size:12px;color:#c2d3e2}.main{padding-top:23px;padding-bottom:40px}.notice{background:#fff6e6;border:1px solid #edd7ae;border-radius:12px;padding:14px 18px;color:#634e29;font-size:14px;margin-bottom:19px}.notice strong{color:#705019}.toolbar{display:flex;gap:10px;align-items:center;margin:0 0 12px}.toolbar input{width:100%;max-width:390px}.toolbar button{white-space:nowrap}input,select,textarea{border:1px solid #cbd6e2;border-radius:9px;padding:9px 12px;color:var(--ink);background:white}.count{color:var(--muted);font-size:13px;margin-bottom:13px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}.card{min-width:0;display:flex;flex-direction:column;gap:12px;border:1px solid var(--line);border-radius:15px;padding:20px;background:white;box-shadow:0 2px 8px #1a294009}.head{display:flex;align-items:center;gap:14px}.logo{width:64px;height:64px;object-fit:cover;border-radius:12px;flex:none}.head h2{font-size:21px;line-height:1.25;margin:0}.group{font-size:12px;color:var(--muted);margin-top:3px}.brief{font-size:14px;color:#445b74;margin:0}.proof{background:#e9f6f1;border-radius:9px;padding:10px 12px;font-size:13px;color:#1d6049}.proof.partial{background:#fff1d9;color:#745014}.caveat{font-size:12px;color:#68778a}.actions{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:auto;font-size:13px}.actions button,.toolbar button,.dialog button{cursor:pointer;background:white;border:1px solid #bbcee4;border-radius:8px;color:var(--blue);padding:8px 11px}.dialog{border:0;border-radius:15px;box-shadow:0 24px 90px #132b4d55;max-width:780px;width:calc(100% - 32px);max-height:88vh;padding:0}.dialog::backdrop{background:#0e254788}.dialogtop{display:flex;align-items:center;gap:14px;padding:17px 23px;border-bottom:1px solid var(--line);position:sticky;top:0;background:white}.dialogtop h2{margin:0;font-size:23px}.dialogtop button{margin-left:auto}.dialogbody{padding:0 23px 25px;overflow:auto}.dialogbody h3{font-size:16px;margin:23px 0 8px}.dialogbody p,.dialogbody li{font-size:14px}.dialogbody ul{padding-left:20px}.evidence a{display:block;margin:7px 0}.dialogbody textarea{width:100%;height:105px;display:block;margin:10px 0}.dialogbody select{width:100%}.fine{color:var(--muted);font-size:12px}footer{font-size:12px;color:var(--muted);margin-top:25px}@media(max-width:950px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:640px){.grid{grid-template-columns:1fr}.wrap{padding-left:18px;padding-right:18px}.hero{padding-top:25px}h1{font-size:29px}.numbers{gap:16px}.number{min-width:0;flex:1}.toolbar{flex-wrap:wrap}.toolbar input{max-width:none}.card{padding:17px}}
</style>
<header class="hero"><div class="wrap"><div class="eyebrow">COZE · 第一批审查</div><h1>核心调用已跑通的 15 款服务插件</h1><p>逐款审查名称、图标和上架文案；每款都能打开 Coze 私有草稿与实际调用证据。14 款核心用例通过，Localization 仅 Markdown 翻译通过。</p><div class="numbers"><div class="number"><strong>14</strong><span>核心用例通过</span></div><div class="number"><strong>1</strong><span>限定模式通过</span></div><div class="number"><strong>0</strong><span>本批正式发布</span></div></div></div></header>
<main class="wrap main"><div class="notice"><strong>这是审查批次，不是上线验收。</strong> 这些证据证明特定 Coze 草稿工具能返回可用结果。完整 MCP 能力、用户一键授权，以及发布后 Agent 安装和调用仍未通过。所有草稿保持未发布；正式发布等你的 review。</div><div class="toolbar"><input id="search" placeholder="搜索插件，例如 Suno、图像或翻译" aria-label="搜索插件"><button id="export">导出本批审查意见</button><a href="./review.html">查看全部 32 款</a></div><div id="count" class="count"></div><div id="grid" class="grid"></div><footer>测试预算上限 200 Credits；实际累计用量以逐项门禁和凭证回读为准。<a href="./e2e-v4/launch-gate.json">查看完整门禁</a> · <a href="https://github.com/AceDataCloud/APIs/pull/956">查看草稿 PR</a></footer></main>
<dialog id="detail" class="dialog"><div id="dialogtop" class="dialogtop"></div><div id="dialogbody" class="dialogbody"></div></dialog>
<script>
const data=PAYLOAD,byId=id=>document.getElementById(id),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let current='';let decisions={};try{decisions=JSON.parse(localStorage.getItem('coze-batch-1-review')||'{}')}catch(_){}
function render(){const q=byId('search').value.trim().toLowerCase(),rows=data.entries.filter(r=>[r.name,r.group,r.brief,r.proof].join(' ').toLowerCase().includes(q));byId('count').textContent=`显示 ${rows.length} / ${data.entries.length} 款。点击“审查”可看完整文案、场景和证据，并留下修改意见。`;byId('grid').innerHTML=rows.map(r=>`<article class="card"><div class="head"><img class="logo" src="${r.icon}" alt="${esc(r.name)} 图标"><div><h2>${esc(r.name)}</h2><div class="group">${esc(r.group)} · ${r.tool_count} 个 HTTP 草稿工具${r.mcp_tool_count?` · MCP 基准 ${r.mcp_tool_count} 个工具`:''}</div></div></div><p class="brief">${esc(r.brief)}</p><div class="proof ${r.partial?'partial':''}">${r.partial?'限定模式通过':'实测通过'}：${esc(r.proof)}</div><div class="caveat">${esc(r.caveat)}</div><div class="actions"><button data-key="${r.key}">审查名字、图标与文案</button><a href="${esc(r.draft_url)}" target="_blank" rel="noreferrer">Coze 草稿 ↗</a></div></article>`).join('');document.querySelectorAll('[data-key]').forEach(b=>b.onclick=()=>openReview(b.dataset.key))}
function openReview(key){current=key;const r=data.entries.find(x=>x.key===key),d=decisions[key]||{};byId('dialogtop').innerHTML=`<img class="logo" src="${r.icon}" alt=""><h2>${esc(r.name)}</h2><button id="close">关闭</button>`;byId('dialogbody').innerHTML=`<h3>名称、图标、上架文案</h3><p><strong>${esc(r.name)}</strong><br>${esc(r.brief)}</p><p>${esc(r.about)}</p><h3>使用场景</h3><ul>${r.scenarios.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><h3>真实 Coze 测试</h3><div class="proof ${r.partial?'partial':''}">${esc(r.proof)}</div><p class="caveat">范围限制：${esc(r.caveat)} 所有草稿尚未正式发布，发布后 Agent E2E 未测。</p><div class="evidence">${r.evidence.map(f=>`<a href="./${esc(f)}" target="_blank">测试证据：${esc(f.split('/').pop())}</a>`).join('')}</div><p><a href="${esc(r.draft_url)}" target="_blank">打开 HTTP 草稿</a>${r.native_url?` · <a href="${esc(r.native_url)}" target="_blank">打开 Suno 原生 MCP 草稿</a>`:''}</p><h3>你的审查意见</h3><p class="fine">保存在本机浏览器；导出后可以发给我。这里的选择不会触发发布。</p><select id="choice"><option value="pending">待审查</option><option value="keep">名称、图标、文案认可</option><option value="change">需要修改</option><option value="hold">暂缓上线</option></select><textarea id="note" placeholder="例如：图标需要调整、文案改法、能力问题">${esc(d.note||'')}</textarea><button id="save">保存意见</button><span id="saved" class="fine"></span>`;byId('choice').value=d.choice||'pending';byId('close').onclick=()=>byId('detail').close();byId('save').onclick=()=>{decisions[current]={choice:byId('choice').value,note:byId('note').value,updated_at:new Date().toISOString()};localStorage.setItem('coze-batch-1-review',JSON.stringify(decisions));byId('saved').textContent=' 已保存在本机'};byId('detail').showModal()}
byId('search').oninput=render;byId('export').onclick=()=>{const a=document.createElement('a'),u=URL.createObjectURL(new Blob([JSON.stringify({batch:1,publication_authorized:false,decisions},null,2)],{type:'application/json'}));a.href=u;a.download='coze-batch-1-review.json';a.click();URL.revokeObjectURL(u)};render();
</script></html>'''.replace('PAYLOAD', payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)
    print(output)


if __name__ == "__main__":
    main()
