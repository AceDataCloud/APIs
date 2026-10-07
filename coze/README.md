# Coze service plugins

This launch review covers 32 API plugins and seven developer/deployment guides.
Names use the service brand, spaces instead of underscores, and `Resolver` for
CAPTCHA services. Fish uses its short brand name. Datasets, Digital Human,
Dreamina, AI Chat and the earlier cross-service Agent concepts are excluded by
`catalog/launch-scope.json`. Historical source snapshots retain provenance and
are not the active launch list.

## Icons

Official brand assets are recorded in `catalog/official-icons.json` and retained
in `icons/official/`. The builder scales originals to a 512px canvas; the review
UI adds no inner padding. Fish uses the clearer matching mark from our Fish MCP,
and Qwen Image uses the official Qwen favicon rather than the generic Alibaba
logo. Gemini, Veo and GLM receive an optical crop of excess white margins
without cutting the brand mark. These three revised draft icons were also
uploaded and checked in Coze on 2026-10-06.

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

## Current release gate (2026-10-07)

Fourteen HTTP plugins have confirmed **Under Review** store submission receipts
following fresh Coze calls and saved credential-redacted examples:

- Wave 1: DeepSeek, Short URL, Google Search, Kimi, GLM and Localization (6 tools).
- Wave 2: Web Extractor, Claude, Grok, Nano Banana and Qwen Image (13 tools).
- Wave 3: OpenAI, Gemini and Fish (13 enabled tools).

Workspace v0.0.2 publication and store submission remain separate from approval,
public discoverability, installation and Agent execution. Those later gates
have not been verified. Store pages and submission receipts are retained in the
local operational evidence, with no production credentials committed here.

Gemini's four tools passed fresh calls. OpenAI's five enabled tools returned text
and completed image results; embeddings returned HTTP 500 and is disabled for
this version. Fish's four enabled tools returned an MP3, voice-list entries and
voice details; custom voice creation returned a reference-audio download error
and is disabled. Both reduced scopes were published as workspace v0.0.2 and
submitted with explicit store-copy limitations. No failed tool was given a
fabricated successful example. Localization remains Markdown/plain-text only;
its store copy explicitly excludes JSON-object translation.

Grok, Gemini and OpenAI task outputs now explicitly retain media URLs, completion
details, costs and errors for single and batch retrieval. The OpenAI import
preserves pagination metadata. Fish voice-list output declares IDs, titles,
license metadata and pagination bounds, so Coze does not return empty entries.
The same completed tasks were read again through Coze after output fixes,
without repeating generation. These changes do not alter provider routing,
authentication or billing rules.

### Earlier validation and scope

The local `e2e-v4/launch-gate.json` evidence file is the
per-service evidence index; the generated review accepts it with
`--e2e-evidence`. Fifteen services have verified real Coze tool calls:
Suno (native MCP generation, task retrieval, two reachable MP3 results),
DeepSeek, Short URL, Google Search, Web Extractor, Kimi, OpenAI, Claude,
Gemini, Grok, GLM, Nano Banana, Qwen Image, Fish and Localization.
Localization is limited to Markdown text translation; JSON-object translation
remains unverified. `build_batch_review.py` creates a separate first-batch
review page with names, icons, copy, draft links and proof for these 15.
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
Gemini, Grok and GLM use chat-only reimports that leave other tools in their
existing drafts. Nano Banana and Qwen Image task results now return image URLs
after Coze output parsing. Fish returns an async task ID, then an audio URL;
both image and audio assets returned HTTP 200.

Localization's union input imported into Coze as an untyped field, so the editor
omitted the required input. A Markdown-only import projection was tested through
Coze and returned Chinese text; JSON-object translation and the earlier direct
API failure remain open.

The documented Coze standard OAuth flow omits a PKCE challenge and sends JSON to
the token endpoint; the hosted MCP OAuth endpoint currently requires PKCE and
form fields. User connection therefore remains blocked. The existing temporary
Suno header was restored to a public invalid metadata marker after the test.
The Suno native MCP draft remains unpublished so it does not expose a connection
that cannot make authenticated calls.

After the user's first-batch publish authorization, 14 HTTP plugins were published
as Coze workspace version v0.0.1: DeepSeek, Short URL, Google Search, Web
Extractor, Claude, OpenAI, Kimi, Gemini, Grok, GLM, Nano Banana, Qwen Image,
Fish and Localization. The latter exposes only the verified Markdown form. This
workspace publication is separate from Plugin Store submission: the store flow
asks for a running example for each tool. The subsequent confirmed submissions
are listed above. Post-publication Agent install and execution remain unverified.
The pre-handoff test credentials were expired and read back. The pre-handoff
ledger was 29.372048470 Credits of the approved 200-Credit cap; continuation
usage is tracked separately in the local credential readbacks.

## Contracts, trials and publication

`plugins/` contains full public HTTP contracts. `imports/` records Coze-compatible
projections for Claude, OpenAI, Kimi, Gemini chat, Grok chat, GLM chat,
Fish TTS and voice listing, Localization Markdown, Nano Banana/Qwen Image tasks,
Grok/Gemini video tasks, OpenAI image tasks, Kling and
Google Search, with explicit limitations.
They are supplementary preparation and do not establish complete MCP parity.
Suno persona deletion is included in the definition, but all destructive and
sensitive fixtures require their own explicit execution scope.

Keep credentials out of prompts, examples, exports and version control. Coze
Request previews can retain a token even after an input field is edited. Build
the saved request with a redacted Authorization value, retain the real response,
then read the persisted example back before publication. Never publish a
real-token example or treat a request template as a successful runtime result.
Imported `Failed` labels before testing are not provider-failure evidence.
Previous API tests do not prove revised native MCP or Coze runtime success.

The user authorized publication of the reviewed first batch on 2026-10-06.
The other 17 plugins are outside that batch. Store submission and Agent E2E
remain open gates for the first batch, as recorded in the local launch gate.
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
python coze/build_batch_review.py --evidence-root /absolute/path/evidence --output /absolute/path/evidence/review-batch-1.html
python -m unittest discover -s tests -v
```

The review builder accepts `--drafts`, `--trials` and `--native-evidence` paths.
Review notes are stored only in the browser and can be exported as JSON; the page
never publishes. Keep private workspace IDs and operational logs outside the repo.
