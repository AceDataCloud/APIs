# Qwen Image 3 API

Generate and edit images with Qwen Image 3 through Ace Data Cloud.

Service page: [Qwen Image 3](https://platform.acedata.cloud/service/qwen-image)

## Models

| Model | Best for |
|---|---|
| `qwen-image-3.0` | Value, throughput, batch production |
| `qwen-image-3.0-pro` | Complex layouts and high-detail output |

## Quick start

```bash
curl -X POST 'https://api.acedata.cloud/qwen-image/images' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen-image-3.0","prompt":"A clean bilingual product poster","size":"1024*1024","n":1}'
```

## APIs

| API | Path | Guide |
|---|---|---|
| Qwen Image API | `/qwen-image/images` | [Integration guide](docs/qwen_image_images_api_integration_guide.md) |
| Qwen Image Tasks API | `/qwen-image/tasks` | [Task guide](docs/qwen_image_tasks_api_integration_guide.md) |

## Related resources

- MCP: `mcp-qwen-image`
- Hosted MCP: `https://qwen-image.mcp.acedata.cloud/mcp`
- CLI: `qwen-image-cli`
