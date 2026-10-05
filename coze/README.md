# Coze service plugins

Prepare one plugin per service, using the service name and the official logo already used by Studio or the public service directory. Datasets and cross-service scene Agents are outside the current launch batch. The dated source snapshot retains catalog provenance, but dataset entries and artwork are excluded from generated launch materials.

The active material covers 35 API services plus seven developer/deployment guides. There are 27 matching dedicated MCPs. **The corresponding MCP business capabilities are the acceptance baseline, not the number of HTTP routes.** Generation, editing, batch retrieval, management, model discovery and usage guidance all count. For example, Suno currently exposes 42 live MCP tools (the local source snapshot has 36); its 18 HTTP operations are a different inventory and do not establish parity.

## Service inventory

| Service plugin | Source MCP tools | Prepared HTTP operations | Contract |
|---|---:|---:|---|
| DeepSeek | No dedicated MCP | 1 | [Definition](plugins/deepseek.yaml) |
| Claude | No dedicated MCP | 3 | [Definition](plugins/claude.yaml) |
| Maestro | 3 | 2 | [Definition](plugins/maestro.yaml) |
| Turnstile | 4 | 2 | [Definition](plugins/turnstile.yaml) |
| Captcha_OCR | 4 | 2 | [Definition](plugins/image2text.yaml) |
| Kimi | No dedicated MCP | 1 | [Definition](plugins/kimi.yaml) |
| Hailuo | 6 | 2 | [Definition](plugins/hailuo.yaml) |
| OpenAI | 15 | 6 | [Definition](plugins/openai.yaml) |
| Gemini | No dedicated MCP | 4 | [Definition](plugins/gemini.yaml) |
| Grok | 8 | 3 | [Definition](plugins/grok.yaml) |
| Veo | 8 | 2 | [Definition](plugins/veo.yaml) |
| AI_Chat | 4 | 2 | [Definition](plugins/aichat.yaml) |
| Google_Search | 11 | 1 | [Definition](plugins/serp.yaml) |
| Luma | 8 | 2 | [Definition](plugins/luma.yaml) |
| Identity_Verification | No dedicated MCP | 10 | [Definition](plugins/identity.yaml) |
| Seedance | 7 | 2 | [Definition](plugins/seedance.yaml) |
| reCAPTCHA | 5 | 4 | [Definition](plugins/recaptcha.yaml) |
| hCaptcha | 5 | 3 | [Definition](plugins/hcaptcha.yaml) |
| Qwen_Image | No dedicated MCP | 2 | [Definition](plugins/qwen-image.yaml) |
| Short_URL | 4 | 1 | [Definition](plugins/shorturl.yaml) |
| Web_Extractor | 5 | 3 | [Definition](plugins/webextrator.yaml) |
| Producer | 18 | 6 | [Definition](plugins/producer.yaml) |
| Nano_Banana | 4 | 2 | [Definition](plugins/nano-banana.yaml) |
| Wan | 7 | 2 | [Definition](plugins/wan.yaml) |
| Dreamina | No dedicated MCP | 2 | [Definition](plugins/dreamina.yaml) |
| Suno | 36 | 18 | [Definition](plugins/suno.yaml) |
| Digital_Human | 5 | 3 | [Definition](plugins/digitalhuman.yaml) |
| HappyHorse | 7 | 2 | [Definition](plugins/happyhorse.yaml) |
| Kling | 10 | 7 | [Definition](plugins/kling.yaml) |
| Localization | No dedicated MCP | 1 | [Definition](plugins/localization.yaml) |
| Fish_Audio | 6 | 5 | [Definition](plugins/fish.yaml) |
| MiniMax | 10 | 2 | [Definition](plugins/minimax.yaml) |
| GLM | 3 | 1 | [Definition](plugins/glm.yaml) |
| Seedream | 6 | 2 | [Definition](plugins/seedream.yaml) |
| FLUX | 6 | 3 | [Definition](plugins/flux.yaml) |

## Assets and capability evidence

- `catalog/official-icons.json` records the Studio constants or public `Service.icon_url` used for each logo. Originals are stored in `icons/official`; `build_icons.py` adapts dimensions without adding badges, captions or recoloring.
- `catalog/mcp-parity.json` records the MCP source revision and every registered tool's parameters and description. Live `tools/list` is the metadata baseline when available; public server cards and the local source snapshot can lag it. None is runtime proof.
- `plugins/` contains the full public HTTP definitions. `imports/` contains documented Coze compatibility projections for Claude, OpenAI, Kling and Google Search. These are supplementary transport preparations, not a claim of complete MCP parity.
- `listings.json` contains service names, briefs, copy, scenarios and privacy fields. `catalog/service-guide.txt` excludes datasets.
- `apps/` retains the earlier textual scene concepts with `launch_scope=false`; they are not part of this launch review or a native Coze export.
- `examples/catalog/validation-cases.json` records per-operation fixtures and authorization requirements. Including a management/deletion definition does not authorize or prove its execution.

`mcp-plugins/` contains the per-server native MCP configuration targets;
`examples/catalog/mcp-validation-cases.json` accounts for every benchmark tool
without granting permission to execute it.

## Coze connection and publication

Use a native MCP plugin when the hosted server and Coze authentication flow are compatible. A Suno MCP draft was prepared separately from the older HTTP draft, but tool sync with no header returned an empty list. The hosted service MCPs intentionally accept direct-client tokens for public metadata discovery and defer actual credential validation to the API. `COZE_METADATA_ONLY_INVALID_TOKEN` is a public invalid marker for draft discovery; it grants no service access and must be replaced by caller-owned authorization before release. Authentication, the actual tool inventory, input fidelity, async completion and error semantics must be verified before claiming parity. Some MCPs exist only as source without a confirmed hosted endpoint.

Never publish a publisher-funded API key. Use caller-owned authorization. No token belongs in prompts, examples, exported workflows or checked-in files. Tests may require an explicitly scoped temporary credential; expire it after the authorized work. Coze debug Request previews can retain a token, so do not save real-token calls as examples.

Workspace publication and store submission are separate actions. Both remain on hold pending user review. Imported tools can display `Failed` before a real debug run; this label is not provider-failure evidence. Existing direct API or earlier Coze tests cannot be reused as proof for the revised native MCP plugins.

## Rebuild

```bash
pip install 'PyYAML>=6,<7' 'openapi-spec-validator>=0.7,<0.8' 'Pillow>=11,<12' 'CairoSVG>=2.7,<3'
python coze/build_catalog.py
python coze/build_imports.py
python coze/build_icons.py
python coze/build_mcp_inventory.py --mcp-root /absolute/path/MCPs --check-live
python coze/build_review.py --output /absolute/path/review.html
python -m unittest discover -s tests -v
```

The review builder accepts `--drafts`, `--trials` and `--native-evidence` paths for local operational evidence. It excludes datasets and the earlier scene Agent concepts, shows each MCP capability target, and saves user review decisions locally with JSON export. It never publishes. Keep workspace IDs, credentials and raw operational logs outside this repository.
