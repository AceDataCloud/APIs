# Coze service plugins

This launch review covers 32 API plugins and seven developer/deployment guides.
Names use the service brand, spaces instead of underscores, and `Resolver` for
CAPTCHA services. Fish uses its short brand name. Datasets, Digital Human,
Dreamina, AI Chat and the earlier cross-service Agent concepts are excluded by
`catalog/launch-scope.json`. Historical source snapshots retain provenance and
are not the active launch list.

## Icons

Official brand assets are recorded in `catalog/official-icons.json` and retained
in `icons/official/`. The builder scales small originals up to the full 512px
canvas; the review UI adds no inner padding. Gemini and Veo receive an optical
crop of excess white margins without cutting the brand mark.

`catalog/icon-overrides.json` selects custom GPT Image 2 utility icons for Identity
Verification, Web Extractor and Localization. Originals are in `icons/custom/`;
the exact prompt set and model are in `catalog/generated-icon-prompts.json`.
These three images were generated through the AceDataCloud GPT Image API and
visually checked before use. They are custom utility artwork, not official
third-party brand logos. No publisher badge or added service-name caption is used.

## MCP capability baseline

Use the full corresponding MCP's business capabilities as the acceptance
baseline, not the number of HTTP routes. The inventory has 25 dedicated MCP
matches, with live tools/list evidence for 21 hosted services. For example,
Suno exposes 42 live tools, while its 18 prepared HTTP operations are a separate
inventory. Generation, editing, batch retrieval, management, model discovery
and usage guidance all count.

| Service plugin | MCP target tools | Prepared HTTP operations | Contract |
|---|---:|---:|---|
| DeepSeek | No dedicated MCP | 1 | [Contract](plugins/deepseek.yaml) |
| Claude | No dedicated MCP | 3 | [Contract](plugins/claude.yaml) |
| Maestro | 3 | 2 | [Contract](plugins/maestro.yaml) |
| Turnstile Resolver | 4 | 2 | [Contract](plugins/turnstile.yaml) |
| CAPTCHA OCR Resolver | 4 | 2 | [Contract](plugins/image2text.yaml) |
| Kimi | No dedicated MCP | 1 | [Contract](plugins/kimi.yaml) |
| Hailuo | 6 | 2 | [Contract](plugins/hailuo.yaml) |
| OpenAI | 15 | 6 | [Contract](plugins/openai.yaml) |
| Gemini | No dedicated MCP | 4 | [Contract](plugins/gemini.yaml) |
| Grok | 8 | 3 | [Contract](plugins/grok.yaml) |
| Veo | 8 | 2 | [Contract](plugins/veo.yaml) |
| Google Search | 11 | 1 | [Contract](plugins/serp.yaml) |
| Luma | 8 | 2 | [Contract](plugins/luma.yaml) |
| Identity Verification | No dedicated MCP | 10 | [Contract](plugins/identity.yaml) |
| Seedance | 7 | 2 | [Contract](plugins/seedance.yaml) |
| reCAPTCHA Resolver | 5 | 4 | [Contract](plugins/recaptcha.yaml) |
| hCaptcha Resolver | 5 | 3 | [Contract](plugins/hcaptcha.yaml) |
| Qwen Image | No dedicated MCP | 2 | [Contract](plugins/qwen-image.yaml) |
| Short URL | 4 | 1 | [Contract](plugins/shorturl.yaml) |
| Web Extractor | 5 | 3 | [Contract](plugins/webextrator.yaml) |
| Producer | 18 | 6 | [Contract](plugins/producer.yaml) |
| Nano Banana | 4 | 2 | [Contract](plugins/nano-banana.yaml) |
| Wan | 8 | 2 | [Contract](plugins/wan.yaml) |
| Suno | 42 | 18 | [Contract](plugins/suno.yaml) |
| HappyHorse | 7 | 2 | [Contract](plugins/happyhorse.yaml) |
| Kling | 15 | 7 | [Contract](plugins/kling.yaml) |
| Localization | No dedicated MCP | 1 | [Contract](plugins/localization.yaml) |
| Fish | 6 | 5 | [Contract](plugins/fish.yaml) |
| MiniMax | 10 | 2 | [Contract](plugins/minimax.yaml) |
| GLM | 3 | 1 | [Contract](plugins/glm.yaml) |
| Seedream | 7 | 2 | [Contract](plugins/seedream.yaml) |
| FLUX | 7 | 3 | [Contract](plugins/flux.yaml) |

`catalog/mcp-parity.json` preserves source and live metadata provenance.
`mcp-plugins/` holds native MCP configuration targets; these are not native Coze
exports. `examples/catalog/mcp-validation-cases.json` references every benchmark
tool without authorizing its execution. Some MCPs have no verified hosted
transport; seven API services have no dedicated corresponding MCP.

The public invalid marker `COZE_METADATA_ONLY_INVALID_TOKEN` may be used only for
metadata discovery on service MCPs that deliberately defer API validation to the
actual service call. It is not a credential and grants no service access. Remove
it and configure caller-owned authorization before release. No paid tools/call
was executed for metadata discovery.

## Current release gate (2026-10-05)

The local `e2e-v4/launch-gate.json` evidence file is the
per-service evidence index; the generated review accepts it with
`--e2e-evidence`. Eight services have verified real Coze tool calls:
Suno (native MCP generation, task retrieval, two reachable MP3 results),
DeepSeek, Short URL, Google Search, Web Extractor, Kimi, OpenAI and Claude.
The 21 hosted MCP inventories and 19 free information calls were direct MCP
checks, separate from Coze execution. The earlier 23-service API batch was
direct API testing, separate from both.

Short URL and Google Search also returned usable results from real Coze draft calls.
Web Extractor originally submitted and completed an owned task, but Coze stripped
its dynamic response object. Its output contract now declares explicit content
fields for single and batch retrieval. The Coze draft was updated and the same
task returned a title, text and Markdown through Coze.

OpenAI, Claude and Kimi exposed a Coze editor problem: it validates required
children of optional nested inputs even when unused. Their text-chat import
projections omit inactive optional objects and message tool-call children while
the canonical public contracts retain them. The three projections were reimported,
their chat tools enabled and real assistant text returned through Coze. This
verifies text chat only; it does not establish their full multimodal/tool parity.

The documented Coze standard OAuth flow omits a PKCE challenge and sends JSON to
the token endpoint; the hosted MCP OAuth endpoint currently requires PKCE and
form fields. User connection therefore remains blocked. The existing temporary
Suno header was restored to a public invalid metadata marker after the test,
and all short-lived test credentials were expired and read back. The corrected
test ledger is 28.477755138 Credits of the approved 200-Credit cap; the earlier
total omitted 0.846 Credits from the initial four-plugin credential. No workspace
publication or store submission was made; post-publication Agent install and
execution remain unverified.

## Contracts, trials and publication

`plugins/` contains full public HTTP contracts. `imports/` records Coze-compatible
projections for Claude, OpenAI, Kimi, Kling and Google Search, with explicit limitations.
They are supplementary preparation and do not establish complete MCP parity.
Suno persona deletion is included in the definition, but all destructive and
sensitive fixtures require their own explicit execution scope.

Keep credentials out of prompts, examples, exports and version control. Coze
Request previews can retain a token; never save real-token runs as examples.
Imported `Failed` labels before testing are not provider-failure evidence.
Previous API tests do not prove revised native MCP or Coze runtime success.

Workspace publication and store submission remain on hold pending user review.
Removed services are excluded from the launch materials; historical private Coze
drafts are not automatically or permanently deleted by these builders.

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

The review builder accepts `--drafts`, `--trials` and `--native-evidence` paths.
Review notes are stored only in the browser and can be exported as JSON; the page
never publishes. Keep private workspace IDs and operational logs outside the repo.
