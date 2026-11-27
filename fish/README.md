# Fish Audio API

Turn text into speech with a saved voice through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/fish/fish_tts) · [Models and pricing](https://platform.acedata.cloud/services/fish?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/fish/fish_tts)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Supply `reference_id` to select a saved voice. See the voice guide for available voices and reference-audio preparation.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/fish/tts \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "text": "Hello! Your first speech request is ready.",
  "format": "mp3"
}'
```

Read `audio_url` from the response. The following fields illustrate a successful result and media URLs are placeholders.

```json
{
  "audio_url": "https://media.example.com/speech.mp3"
}
```

Open or download the URL returned by your own request.

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/fc541fac-a941-47fd-b6f7-48d6cb9da523?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |
| [Fish Model Create API](https://platform.acedata.cloud/documents/82dcabe9-b1a3-541f-80f1-decb183b920c?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/fish/model` | Create a custom voice model from reference audio |
| [Fish Model Query API](https://platform.acedata.cloud/documents/0a2c983b-e20f-5926-a45f-07b61373617d?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/fish/model` | List voice models |
| [Fish Model Get API](https://platform.acedata.cloud/documents/70f84537-7c48-57d3-9a21-b2a4f55e8f31?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/fish/model/{id}` | Fetch a single voice model |

## Voices and reference audio

For a saved voice, set `reference_id` in the TTS request. See [TTS and one-shot reference audio](docs/fish_tts_api_integration_guide.md) and [voice model management](https://docs.acedata.cloud/en/guides/fish/fish_model) for preparation and supported options.

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
