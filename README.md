# Ace Data Cloud APIs

English API guides and runnable examples for chat, images, music, video, speech and developer tools. Choose a service below, get an application API key, then follow its Quickstart to the result.

[Get an API key](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [API documentation](https://platform.acedata.cloud/documents?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Store the copied key in the `ACEDATACLOUD_API_KEY` environment variable on your server. Replace `YOUR_API_KEY` below with the copied value. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/v1/chat/completions \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"model":"gpt-6-luna","messages":[{"role":"user","content":"Say hello in one sentence."}]}'
```

### Response JSON

Illustrative response. Read `choices[0].message.content` for the answer.

```json
{
  "id": "chatcmpl-example",
  "object": "chat.completion",
  "created": 1790000000,
  "model": "gpt-6-luna",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## APIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaAPI](https://github.com/AceDataCloud/LumaAPI) | Luma video generation API docs |
| `maestro/` | [MaestroAPI](https://github.com/AceDataCloud/MaestroAPI) | Maestro end-to-end AI video production API docs |
| `tripo/` | [TripoAPI](https://github.com/AceDataCloud/TripoAPI) | Tripo 3D generation, models, animations and task lookup |
| `acemusic/` | [ACEMusicAPI](https://github.com/AceDataCloud/ACEMusicAPI) | ACE Music song and lyrics generation API docs |
| `suno/` | [SunoAPI](https://github.com/AceDataCloud/SunoAPI) | Suno music generation API docs |
| `sora/` | [SoraAPI](https://github.com/AceDataCloud/SoraAPI) | Retired; migration guidance and historical documentation |
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
| `face/` | [FaceAPI](https://github.com/AceDataCloud/FaceAPI) | Historical reference; check current service availability |
| `shorturl/` | [ShortURLAPI](https://github.com/AceDataCloud/ShortURLAPI) | Short URL API docs |
| `webextrator/` | [WebExtratorAPI](https://github.com/AceDataCloud/WebExtratorAPI) | Web extraction and rendering API docs |
| `aichat/` | [AiChatAPI](https://github.com/AceDataCloud/AiChatAPI) | AI Dialogue (multi-model chat) API docs |
| `grok/` | [GrokAPI](https://github.com/AceDataCloud/GrokAPI) | Grok chat completions API docs |
| `glm/` | [GlmAPI](https://github.com/AceDataCloud/GlmAPI) | GLM chat completions API docs |
| `kimi/` | [KimiAPI](https://github.com/AceDataCloud/KimiAPI) | Kimi chat completions API docs |
| `coze/` | [CozeAPI](https://github.com/AceDataCloud/CozeAPI) | Importable OpenAPI plugin schemas for Coze / 扣子 |
| `deepseek/` | [DeepSeekAPI](https://github.com/AceDataCloud/DeepSeekAPI) | [deepseek API quickstart](deepseek/README.md) |
| `mimo/` | [MiMoAPI](https://github.com/AceDataCloud/MiMoAPI) | [mimo API quickstart](mimo/README.md) |
| `dreamina/` | [DreaminaAPI](https://github.com/AceDataCloud/DreaminaAPI) | [dreamina API quickstart](dreamina/README.md) |
| `digitalhuman/` | [DigitalHumanAPI](https://github.com/AceDataCloud/DigitalHumanAPI) | [digitalhuman API quickstart](digitalhuman/README.md) |
| `turnstile/` | [TurnstileAPI](https://github.com/AceDataCloud/TurnstileAPI) | [turnstile API quickstart](turnstile/README.md) |
| `recaptcha/` | [ReCaptchaAPI](https://github.com/AceDataCloud/ReCaptchaAPI) | [recaptcha API quickstart](recaptcha/README.md) |
| `hcaptcha/` | [HCaptchaAPI](https://github.com/AceDataCloud/HCaptchaAPI) | [hcaptcha API quickstart](hcaptcha/README.md) |
| `image2text/` | [Image2TextAPI](https://github.com/AceDataCloud/Image2TextAPI) | [image2text API quickstart](image2text/README.md) |
| `identity/` | [IdentityAPI](https://github.com/AceDataCloud/IdentityAPI) | [identity API quickstart](identity/README.md) |
| `localization/` | [LocalizationAPI](https://github.com/AceDataCloud/LocalizationAPI) | [localization API quickstart](localization/README.md) |

## MCP Servers

Ace Data Cloud provides [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers, allowing AI assistants like Claude, Cursor, Windsurf, and others to directly call our APIs.

> [!TIP]
> This section introduces the active MCP servers provided by Ace Data Cloud. Documentation links point to the canonical pages on the Ace Data Cloud platform.

| MCP Server | Docs |
|---|---|
| Tripo 3D MCP Server | [Package and setup](https://pypi.org/project/mcp-tripo/) |
| ACE Music MCP Server | [View documentation](https://platform.acedata.cloud/documents/mcp-acemusic?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Flux MCP Server | [View documentation](https://platform.acedata.cloud/documents/flux-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Luma MCP Server | [View documentation](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Nanobanana MCP Server | [View documentation](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Seedance MCP Server | [View documentation](https://platform.acedata.cloud/documents/seedance-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Seedream MCP Server | [View documentation](https://platform.acedata.cloud/documents/seedream-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Serp MCP Server | [View documentation](https://platform.acedata.cloud/documents/serp-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Shorturl MCP Server | [View documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Suno MCP Server | [View documentation](https://platform.acedata.cloud/documents/suno-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| Veo MCP Server | [View documentation](https://platform.acedata.cloud/documents/veo-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |

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

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.

The read-only user flag `has_recharged` records this eligibility; it is not a request parameter. Realtime connection authentication does not occupy this ordinary-request slot and retains its existing per-turn billing.

Mirrors marked `create_missing: true` are provisioned as public repositories by the post-merge sync. This includes the newly added service packages and the Qwen Image mapping. Each service README remains independently readable from its mirror.
