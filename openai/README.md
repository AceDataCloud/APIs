# OpenAI API

Generate text and build conversations with OpenAI models through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/openai-chat-completions-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/openai?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/openai-chat-completions-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application**. If it is missing, select **Initialize General Application**. Use the copy button marked **1** to copy its API key. Confirm service access and enough balance for your first request.

![General Application with the API key copy button marked 1 and Manage Keys marked 2](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

For a separate key, select **Manage Keys** (marked **2**) → **Create**. Enter a name for your integration, review optional usage limits, expiration and allowed APIs, then select **Create**. The screenshot uses an example name.

![Create New Credential with a name, optional restrictions and the Create button](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

3. Copy the raw key value and save it in your terminal environment. The HTTP examples add the `Bearer` prefix for you.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

[Step-by-step API key guide](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/openai/chat/completions \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "gpt-6.2-sol",
  "messages": [
    {
      "role": "user",
      "content": "Explain what an API is in one sentence."
    }
  ],
  "stream": false
}'
```

Read `choices[0].message.content` from the response. The following fields illustrate a successful result.

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "An API lets software request data or actions from another service."
      }
    }
  ]
}
```

## Generate an image with GPT Image 2.6

Use `gpt-image-2.6-flare` for this first image. Compare the available GPT Image 2.6 model options and prices in the [model directory](https://platform.acedata.cloud/models/gpt-image-2.6-flare?m=image&utm_source=github&utm_medium=referral&utm_campaign=evergreen).

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/openai/images/generations \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "gpt-image-2.6-flare",
  "prompt": "A blue ceramic coffee mug on a white table, soft morning light, product photograph",
  "response_format": "url"
}'
```

Open `data[0].url` from the response. For reference-image edits, use the [image editing guide](docs/openai_images_edits_api_integration_guide.md).

## APIs and Guides

Explore the supported endpoints and integration guides for OpenAI generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [OpenAI Chat Completions API](https://platform.acedata.cloud/documents/openai-chat-completions?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/openai/chat/completions` | [OpenAI Chat Completion API Integration Guide](https://platform.acedata.cloud/documents/openai-chat-completions-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [OpenAI Images Generations API](https://platform.acedata.cloud/documents/openai-images-generations?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/openai/images/generations` | [OpenAI Images Generations API Integration Guide](https://platform.acedata.cloud/documents/openai-images-generations-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [OpenAI Responses API](https://platform.acedata.cloud/documents/openai-responses?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/openai/responses` | [OpenAI Responses API Integration Guide](https://platform.acedata.cloud/documents/openai-v1-responses-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [OpenAI Embeddings API](https://platform.acedata.cloud/documents/openai-embeddings?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/openai/embeddings` | [OpenAI Embeddings API Integration Guide](docs/openai_embeddings_api_integration_guide.md) |
| [OpenAI Images Edits API](https://platform.acedata.cloud/documents/openai-images-edits?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/openai/images/edits` | [OpenAI Images Edits API Integration Guide](https://platform.acedata.cloud/documents/openai-images-edits-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |

## Chat and Responses Billing

Accepted compatible-model requests on `/openai/chat/completions` (alias `/v1/chat/completions`) and `/openai/responses` (alias `/v1/responses`) are billed for the selected model's input, output, and cache usage, not a fixed fee for switching API formats. Chat Completions `usage.prompt_tokens` and Responses `usage.input_tokens` include cached tokens; reported cache usage is charged at the corresponding cache rates. Check the console's current model prices and the response's `usage.cost` when present. See the [Chat Completions guide](docs/openai_chat_completion_api_integration_guide.md#token-and-cache-billing) and [Responses guide](docs/openai_responses_api_integration_guide.md#token-and-cache-billing) for details.

## Regional catalog availability

The OpenAI image generation and editing APIs and their companion guides are hidden from the mainland-China catalog. Check the catalog available to your region before following the image examples below; these global reference examples do not establish regional availability.

## Troubleshooting

- For authentication errors, check the copied API key, service access, expiration and configured usage limits. [API key guide](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.

Realtime connection authentication does not occupy this ordinary-request slot and retains its existing per-turn billing.
