# AceDataCloud APIs

Monorepo for all AceDataCloud API documentation repositories.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## APIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaAPI](https://github.com/AceDataCloud/LumaAPI) | Luma video generation API docs |
| `maestro/` | [MaestroAPI](https://github.com/AceDataCloud/MaestroAPI) | Maestro end-to-end AI video production API docs |
| `suno/` | [SunoAPI](https://github.com/AceDataCloud/SunoAPI) | Suno music generation API docs |
| `sora/` | [SoraAPI](https://github.com/AceDataCloud/SoraAPI) | Sora video generation API docs |
| `veo/` | [VeoAPI](https://github.com/AceDataCloud/VeoAPI) | Veo video generation API docs |
| `flux/` | [FluxAPI](https://github.com/AceDataCloud/FluxAPI) | Flux image generation API docs |
| `happyhorse/` | [HappyHorseAPI](https://github.com/AceDataCloud/HappyHorseAPI) | Happy Horse video generation and editing API docs |
| `serp/` | [SerpAPI](https://github.com/AceDataCloud/SerpAPI) | Web search API docs |
| `nanobanana/` | [NanoBananaAPI](https://github.com/AceDataCloud/NanoBananaAPI) | NanoBanana image generation API docs |
| `openai/` | [OpenAIAPI](https://github.com/AceDataCloud/OpenAIAPI) | OpenAI-compatible API docs |
| `wan/` | [WanAPI](https://github.com/AceDataCloud/WanAPI) | Wan (Tongyi Wanxiang) video generation API docs |
| `seedance/` | [SeedanceAPI](https://github.com/AceDataCloud/SeedanceAPI) | Seedance (ByteDance) video generation API docs |
| `qwen-image/` | [QwenImageAPI](https://github.com/AceDataCloud/QwenImageAPI) | Qwen Image 3 generation and editing API docs |
| `seedream/` | [SeedreamAPI](https://github.com/AceDataCloud/SeedreamAPI) | Seedream (ByteDance) image generation API docs |
| `kling/` | [KlingAPI](https://github.com/AceDataCloud/KlingAPI) | Kling video generation API docs |
| `hailuo/` | [HailuoAPI](https://github.com/AceDataCloud/HailuoAPI) | Hailuo video generation API docs |
| `producer/` | [ProducerAPI](https://github.com/AceDataCloud/ProducerAPI) | Producer music generation API docs |
| `claude/` | [ClaudeAPI](https://github.com/AceDataCloud/ClaudeAPI) | Claude chat completions API docs |
| `gemini/` | [GeminiAPI](https://github.com/AceDataCloud/GeminiAPI) | Gemini chat completions API docs |
| `fish/` | [FishAPI](https://github.com/AceDataCloud/FishAPI) | Fish Audio TTS and voice cloning API docs |
| `face/` | [FaceAPI](https://github.com/AceDataCloud/FaceAPI) | Face transformation API docs |
| `shorturl/` | [ShortURLAPI](https://github.com/AceDataCloud/ShortURLAPI) | Short URL API docs |
| `webextrator/` | [WebExtratorAPI](https://github.com/AceDataCloud/WebExtratorAPI) | Web extraction and rendering API docs |
| `aichat/` | [AiChatAPI](https://github.com/AceDataCloud/AiChatAPI) | AI Dialogue (multi-model chat) API docs |
| `grok/` | [GrokAPI](https://github.com/AceDataCloud/GrokAPI) | Grok chat completions API docs |
| `glm/` | [GlmAPI](https://github.com/AceDataCloud/GlmAPI) | GLM chat completions API docs |
| `kimi/` | [KimiAPI](https://github.com/AceDataCloud/KimiAPI) | Kimi chat completions API docs |
| `coze/` | [CozeAPI](https://github.com/AceDataCloud/CozeAPI) | Importable OpenAPI plugin schemas for Coze / 扣子 |

## MCP Servers

Ace Data Cloud provides [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers, allowing AI assistants like Claude, Cursor, Windsurf, and others to directly call our APIs.

> [!TIP]
> This section introduces the active MCP servers provided by Ace Data Cloud. Documentation links point to the canonical pages on the Ace Data Cloud platform.

| MCP Server | Docs |
|---|---|
| Flux MCP Server | [View documentation](https://platform.acedata.cloud/documents/flux-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_flux_mcp) |
| Luma MCP Server | [View documentation](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_luma_mcp) |
| Nanobanana MCP Server | [View documentation](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_nano_banana_mcp) |
| Seedance MCP Server | [View documentation](https://platform.acedata.cloud/documents/seedance-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_seedance_mcp) |
| Seedream MCP Server | [View documentation](https://platform.acedata.cloud/documents/seedream-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_seedream_mcp) |
| Serp MCP Server | [View documentation](https://platform.acedata.cloud/documents/serp-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_serp_mcp) |
| Shorturl MCP Server | [View documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_short_url_mcp) |
| Suno MCP Server | [View documentation](https://platform.acedata.cloud/documents/suno-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_suno_mcp) |
| Veo MCP Server | [View documentation](https://platform.acedata.cloud/documents/veo-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=catalog_api_readme_documents_veo_mcp) |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.

## Documentation updates

PlatformBackend's daily ecosystem CronJob prepares incremental capability PRs
using a pinned Backend source. Existing CI and human review gate each update.
The previous dispatch/Copilot sync workflows are retired.

Standalone API repositories are mirrors of this monorepo. Backend's old
`repo.py` writer is retired; all documentation changes originate here.

## Daily capability updates

PlatformBackend `ecosystem.py` is the only scheduled coordinator.
One daily Kubernetes Job reviews Backend docs and API changes with Claude Code,
updates existing files, and creates or updates one reviewable PR per repository.
It never merges PRs or duplicates the Backend guide tree. Normal CI and review
remain required; publication and sub-repository mirroring run after merge.

Entries marked `metadata: true` in `sync.yaml` also let Backend ecosystem.py
maintain GitHub description, homepage and topics from the public service catalog.
This opt-in preserves the old repo.py coverage without changing repository files;
private/retired services are skipped.
