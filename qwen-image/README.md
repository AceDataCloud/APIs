# Qwen Image 3 API

Generate and edit images with Qwen Image 3 through Ace Data Cloud.

Service page: [Qwen Image 3](https://platform.acedata.cloud/services/9a33d10b-9f5d-438f-9701-c34906a2d891?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=qwen_image_api_readme_service_qwen_image)

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=qwen_image_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=qwen_image_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

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
