# AceDataCloud APIs

Monorepo for all AceDataCloud API documentation repositories.

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
> This section introduces the MCP servers provided by Ace Data Cloud, supporting information exchange and integration among multiple AI assistants.

| MCP Server | Docs |
|---|---|
| Flux MCP Server | [docs.acedata.cloud/mcp/flux](https://docs.acedata.cloud/mcp/flux) |
| Luma MCP Server | [docs.acedata.cloud/mcp/luma](https://docs.acedata.cloud/mcp/luma) |
| Nanobanana MCP Server | [docs.acedata.cloud/mcp/nanobanana](https://docs.acedata.cloud/mcp/nanobanana) |
| Seedance MCP Server | [docs.acedata.cloud/mcp/seedance](https://docs.acedata.cloud/mcp/seedance) |
| Seedream MCP Server | [docs.acedata.cloud/mcp/seedream](https://docs.acedata.cloud/mcp/seedream) |
| Serp MCP Server | [docs.acedata.cloud/mcp/serp](https://docs.acedata.cloud/mcp/serp) |
| Shorturl MCP Server | [docs.acedata.cloud/mcp/shorturl](https://docs.acedata.cloud/mcp/shorturl) |
| Sora MCP Server | [docs.acedata.cloud/mcp/sora](https://docs.acedata.cloud/mcp/sora) |
| Suno MCP Server | [docs.acedata.cloud/mcp/suno](https://docs.acedata.cloud/mcp/suno) |
| Veo MCP Server | [docs.acedata.cloud/mcp/veo](https://docs.acedata.cloud/mcp/veo) |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.
