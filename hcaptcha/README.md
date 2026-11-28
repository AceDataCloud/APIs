# hCaptcha API

Request a verification token for your website integration through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/captcha-token-hcaptcha-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/hcaptcha?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/captcha-token-hcaptcha-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Replace `website_url` and `website_key` with the page URL and site key from the website integration you are testing.

### Request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/captcha/token/hcaptcha \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "website_url": "https://YOUR_WEBSITE",
  "website_key": "YOUR_WEBSITE_KEY"
}'
```

### Response JSON

Illustrative response with placeholder identifiers and output values.

```json
{
  "token": "VERIFICATION_TOKEN",
  "elapsed": 12.4
}
```

Use the `token` returned by your request. `elapsed` is the processing time in seconds.

## API reference

- [`/captcha/tasks`](https://platform.acedata.cloud/documents/captcha-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/captcha/recognition/hcaptcha`](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/captcha/token/hcaptcha`](https://platform.acedata.cloud/documents/captcha-token-hcaptcha?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
