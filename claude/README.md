# Claude API

Generate text and build conversations with Claude models through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/claude-chat-completion-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/claude?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/claude-chat-completion-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

### Request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/v1/messages \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "claude-sonnet-5-5",
  "messages": [
    {
      "role": "user",
      "content": "Explain what an API is in one sentence."
    }
  ],
  "stream": false,
  "max_tokens": 128
}'
```

### Response JSON

Illustrative response with placeholder identifiers and output values.

```json
{
  "id": "msg_example",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-5-5",
  "content": [
    {
      "type": "text",
      "text": "An API lets software request data or actions from another service."
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 18,
    "output_tokens": 15
  }
}
```

Read `content[0].text` for the answer and `usage` for token counts.

## APIs and Guides

Explore the supported endpoints and integration guides for Claude.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Claude Chat Completion API](https://platform.acedata.cloud/documents/claude-chat-completions?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/v1/chat/completions` | [Claude Chat Completion API Integration Guide](docs/claude_chat_completions_api_integration_guide.md) |
| [Claude Messages API](https://platform.acedata.cloud/documents/claude-chat-completions?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/v1/messages` | [Claude Messages API Integration Guide](docs/claude_messages_api_integration_guide.md) |
| [Claude Messages Count Tokens API](https://platform.acedata.cloud/documents/claude-messages-count-tokens?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/v1/messages/count_tokens` | [Claude Messages Count Tokens API Integration Guide](docs/claude_messages_count_tokens_api_integration_guide.md) |

## GPT-6.2 on Messages

Select `gpt-6.2-astra` or `gpt-6.2-sol` on `/v1/messages` while keeping the Messages request and response format. Send `messages` and `max_tokens`, and read the returned `content` and `usage` fields. Check the selected model's current pricing and account availability; model-specific Claude features depend on the selected model. See the [Messages guide](docs/claude_messages_api_integration_guide.md#basic-usage).

## Claude Fable 5.2

Use the exact model ID `claude-fable-5-2` on Messages or Chat Completions. Prefer Messages for native thinking blocks and tool interaction. Adaptive thinking remains on; omit `temperature`, `top_p`, and `top_k`, use automatic tool choice, and provide enough `max_tokens` for both thinking and final text. This model currently does not support the Count Tokens or Responses endpoints on Ace Data Cloud.

At the current maximum package (142,800 Credits for $13,584), standard input costs $3.20 and output costs $16 per million tokens. Cache reads cost $0.08, five-minute cache writes $4, and one-hour cache writes $6.40 per million tokens. These are 40% of Anthropic's standard API rates (60% lower) at that package rate; other packages and account discounts must be checked on the [live pricing page](https://platform.acedata.cloud/models/claude-fable-5-2?m=chat&tab=pricing&utm_source=github).

## Token and Cache Billing

Compatible model requests accepted by the platform are billed for the selected model's input, output, and cache usage, not a fixed fee for switching API formats. Chat Completions `usage.prompt_tokens` includes cached tokens, with reported cache usage charged at the corresponding cache rates. Messages `usage.input_tokens` excludes separately reported cache-read and cache-creation tokens, which are settled separately. Check the console's current model prices and the response's `usage.cost` when present; Messages streaming responses may omit `cost` or return it as null. See the [Messages guide](docs/claude_messages_api_integration_guide.md#basic-usage) for the usage fields.

## Troubleshooting

- For authentication errors, open [Manage Keys](https://platform.acedata.cloud/console/credentials?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) to check the key’s allowed APIs, expiration and usage limit.
- If the application balance is insufficient, click **Top Up** on its card.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
