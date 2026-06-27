# AceDataCloud APIs

Monorepo for all AceDataCloud API documentation repositories.

## APIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaAPI](https://github.com/AceDataCloud/LumaAPI) | Luma video generation API docs |
| `suno/` | [SunoAPI](https://github.com/AceDataCloud/SunoAPI) | Suno music generation API docs |
| `sora/` | [SoraAPI](https://github.com/AceDataCloud/SoraAPI) | Sora video generation API docs |
| `veo/` | [VeoAPI](https://github.com/AceDataCloud/VeoAPI) | Veo video generation API docs |
| `flux/` | [FluxAPI](https://github.com/AceDataCloud/FluxAPI) | Flux image generation API docs |
| `serp/` | [SerpAPI](https://github.com/AceDataCloud/SerpAPI) | Web search API docs |
| `nanobanana/` | [NanoBananaAPI](https://github.com/AceDataCloud/NanoBananaAPI) | NanoBanana image generation API docs |
| `openai/` | [OpenAIAPI](https://github.com/AceDataCloud/OpenAIAPI) | OpenAI-compatible API docs |
| `pixverse/` | [PixverseAPI](https://github.com/AceDataCloud/PixverseAPI) | Pixverse video generation API docs |
| `wan/` | [WanAPI](https://github.com/AceDataCloud/WanAPI) | Wan (Tongyi Wanxiang) video generation API docs |
| `aichat/` | — | AI Dialogue (multi-model chat) API docs |

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
