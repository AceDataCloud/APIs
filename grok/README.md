# Grok API

Generate text and build conversations with Grok models through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/grok/grok_chat_completions) · [Models and pricing](https://platform.acedata.cloud/services/grok?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/grok/grok_chat_completions)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/grok/chat/completions \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "grok-4.7",
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

## APIs and Guides

Explore the supported endpoints and integration guides for Grok.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Grok Chat Completion API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/grok/chat/completions` | [Grok Chat Completion API Integration Guide](docs/grok_chat_completions_api_integration_guide.md) |

## Troubleshooting

- For authentication errors, check the copied API key, service access, expiration and configured usage limits. [API key guide](https://docs.acedata.cloud/en/authentication)
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
