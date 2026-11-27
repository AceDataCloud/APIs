# AI Chat API

Build model conversations and agent workflows with the AI Chat v2 API.

[API documentation](https://platform.acedata.cloud/documents/aichat2-conversations-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/aichat?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/aichat2-conversations-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. If needed, select **Initialize General Application** first. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

[API key help](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Quickstart

### Request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/aichat2/conversations \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "chat",
  "model": "gpt-6.2-sol",
  "question": "Explain what an API is in one sentence.",
  "stateful": false,
  "max_turns": 1
}'
```

### Response JSON

Illustrative response with placeholder identifiers and output values.

```json
{
  "id": "CONVERSATION_ID",
  "answer": "An API lets software request data or actions from another service."
}
```

Read `answer` for the reply. The `id` identifies this conversation result.

## APIs and Guides

Explore the supported endpoints and integration guides for AI Chat.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [AI Chat Conversations API](https://platform.acedata.cloud/documents/aichat-conversations?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/aichat/conversations` | [AI Chat Conversations API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |

## Gemini 4 Neon with AI Chat v2

Send a question to `POST /aichat2/conversations` using your application API key:

```json
{"action":"chat","model":"gemini-4-neon","question":"Summarize the three release milestones.","stateful":false}
```

The `answer` field contains the reply. The response includes token usage.

## AI Chat v2 Execution Limits

[AI Chat v2](https://platform.acedata.cloud/documents/aichat2-conversations?utm_source=github&utm_medium=referral&utm_campaign=evergreen) supports agent tool calls. Its `model` field includes `gpt-6.2-astra`, `gpt-6.2-sol`, `claude-fable-5-2` and `kimi-k3.1-pro`, with `claude-fable-5-1`, `claude-fable-5`, and `kimi-k3` still available. The Kimi options also include `kimi-k2.6` and `kimi-k2.7-code`. Use the `chatgpt` model group for the GPT models and follow the v2 conversation payload. This is the v2 model list, not the separate `/aichat/conversations` model list documented above.

The following limits apply to v2, not the `/aichat/conversations` endpoint documented above.

| Endpoint | Optional field | Range | Default when omitted |
| --- | --- | --- | --- |
| `POST /aichat2/conversations` | `max_turns` | 1–500 | 500 |
| `POST /aichat2/scheduled-tasks` | `template.max_turns` | 1–500 | 500 |

Setting `max_turns` to `1` requests a single answer without tool calls. For scheduled tasks, `template.max_turns` limits agent turns per run, not scheduling frequency. Each model call is still billed for actual usage; 500 is an upper bound, and a run may end earlier due to timeout, authorization, or other execution conditions.

Repeated AI execution failures do not automatically pause a scheduled task: it will try again at the next scheduled time. Automatic pausing occurs after five consecutive failures to hand the task to the execution service. Insufficient balance marks a run as failed and triggers a recharge notification. An enabled task does not mean its latest run succeeded; check run history with `action: "retrieve_runs"` on `POST /aichat2/scheduled-tasks` for execution results.

## Scheduled Task Timing and Accounts

Use `POST /aichat2/scheduled-tasks` for these v2 controls, not `/aichat/conversations`.

| Field | Behavior |
| --- | --- |
| `jitter_seconds` | Nonnegative integer seconds; defaults to `60`. Automatic cloud runs get an independent random offset before or after their planned time; `0` disables it. For interval schedules, the range is capped at one quarter of `interval_seconds`. Local and manual runs have no jitter. |
| `trigger_probability` | Number from `0` to `1`, default `1`. Each account independently decides whether to start at each automatic scheduled trigger: `0` skips all automatic attempts but still allows manual runs, `1` always starts, and `0.5` starts about half the attempts over time, not necessarily half the accounts each round. Applies to automatic cloud and local runs, independently of jitter; manual runs do not sample probability. |
| `unattended_policy.connection_bindings` | Cloud tasks can select multiple accounts for one connector, with one account each for other connectors, up to 100 bindings total. Local execution still permits only one account per connector. |

For example, update an existing task with your installed skill and connected account IDs:

```json
{
  "action": "update",
  "id": "YOUR_TASK_ID",
  "jitter_seconds": 600,
  "trigger_probability": 0.5,
  "unattended_policy": {
    "allowed_skills": ["your-installed-skill"],
    "connection_bindings": [
      {"connector_identifier": "github/github", "connection_id": "account-one"},
      {"connector_identifier": "github/github", "connection_id": "account-two"}
    ]
  }
}
```

Each selected cloud account has its own schedule, conversation, authorization check, billing, and run result. One account's failure does not block the others. For automatic runs with jitter disabled, accounts share a planned time but are processed sequentially, not guaranteed to start simultaneously. The task list retains one configuration and shows the account count and earliest next trigger.

For automatic scheduled runs, probability is sampled before conversation creation, model calls, and model charges. A skipped attempt records `status: "skipped"` and `error_code: "probability_skipped"`, does not pause the task, and incurs no model charge. Duplicate callbacks reuse the saved decision rather than sampling again.

Changing saved account selection reschedules the next execution; editing the prompt or probability does not. Pause, resume, and delete affect all accounts, while already-started runs may finish. Existing single-account tasks retain their settings; multi-account selection does not merge copied tasks, so pause redundant copies to avoid duplicate runs. In run history, `run_accounts` snapshots only the accounts selected for that run; later binding changes do not rewrite it.

### Manually Trigger Selected Accounts

On `POST /aichat2/scheduled-tasks`, use `action: "trigger_selected"` to run only selected accounts for this invocation:

```json
{
  "action": "trigger_selected",
  "id": "YOUR_TASK_ID",
  "connection_ids": ["account-one"]
}
```

`connection_ids` is required and must be a nonempty array without duplicates. Select only accounts already saved for the task's multi-account connector; fixed accounts for other connectors remain bound to each run. An out-of-scope account, including one removed from the task, rejects the entire request without starting any runs. The existing `action: "trigger"` without an account list still attempts all configured accounts. If an older server does not support `trigger_selected`, it returns an error; do not fall back to triggering all accounts.

Manual runs bypass `jitter_seconds` and do not wait for the previous account to finish. Each selected account starts without sampling the saved `trigger_probability`, even when it is `0`; unselected accounts get no run records. This also applies to single-account immediate triggers, `action: "trigger"`, and local manual runs. Saved account bindings, trigger probability, and the next automatic schedule remain unchanged; authorization checks and normal billing still apply.

When a cloud manual trigger is accepted, the API returns `runs`, each with `run_id`, `status: "queued"`, and `conversation_id`. `triggered_count` is the number of accounts started; the compatibility field `skipped_count` is always `0`. Top-level compatibility fields refer to the first started run. Each manual run records its effective `trigger_probability` as `1`, without rewriting task configuration or historical records. Acceptance does not mean execution has completed successfully.

In Nexior, a multi-account task's immediate-trigger control opens an account picker with nothing selected by default; choose one or more accounts or select all. Single-account tasks trigger directly. Starting one account opens its conversation; starting multiple accounts shows the task's run history.

## Search Scheduled Tasks

On `POST /aichat2/scheduled-tasks`, use `action: "retrieve_batch"` to list the current user's tasks, newest first. Optional `search` matches task-name substrings, ignoring English case and surrounding whitespace; it is not a regular expression. Omit it or send an empty string for all tasks. Search runs before pagination across the user's complete task list.

Request body example (use the same authenticated request setup as above):

```json
{"action": "retrieve_batch", "search": "daily", "offset": 0, "limit": 10}
```

`offset` defaults to `0`; `limit` defaults to `100` and must be 1–100. Read the current page from `items` and the total matching count from `count`. Increase `offset` by `limit`, keeping `search` unchanged, until the accumulated results reach `count`.

## MiMo

`mimo-v2.6-pro` and `mimo-v2.6-flash` support text chat, reasoning and function tools. Consult the console for service status and account access. The dedicated contract is `POST /mimo/chat/completions`, with the permitted `/v1/chat/completions` alias. AiChat v2 uses its own conversation payload and the `mimo` model group.

See the [MiMo integration guide](docs/mimo_chat_completions_integration_guide.md) for request shape and billing semantics.

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
