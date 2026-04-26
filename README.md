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
| `midjourney/` | [MidjourneyAPI](https://github.com/AceDataCloud/MidjourneyAPI) | Midjourney image generation API docs |
| `serp/` | [SerpAPI](https://github.com/AceDataCloud/SerpAPI) | Web search API docs |
| `nanobanana/` | [NanoBananaAPI](https://github.com/AceDataCloud/NanoBananaAPI) | NanoBanana image generation API docs |
| `openai/` | [OpenAIAPI](https://github.com/AceDataCloud/OpenAIAPI) | OpenAI-compatible API docs |
| `pixverse/` | [PixverseAPI](https://github.com/AceDataCloud/PixverseAPI) | Pixverse video generation API docs |
| `aichat/` | — | AI Dialogue (multi-model chat) API docs |
| `overview/` | — | MCP servers overview |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.
