# reCAPTCHA API

Request a verification token for your website integration through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/recaptcha/captcha_token_recaptcha2) · [Models and pricing](https://platform.acedata.cloud/services/recaptcha?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/recaptcha/captcha_token_recaptcha2)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Replace `website_url` and `website_key` with the page URL and site key from the website integration you are testing.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/captcha/token/recaptcha2 \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "website_url": "https://YOUR_WEBSITE",
  "website_key": "YOUR_WEBSITE_KEY"
}'
```

Read `token` from the response. The following fields illustrate a successful result.

```json
{
  "token": "VERIFICATION_TOKEN",
  "elapsed": 12.4
}
```

## API reference

- [`/captcha/recognition/recaptcha2`](https://platform.acedata.cloud/documents/cadfc74b-e737-462a-8a04-5cbb1e18cbf6?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/captcha/token/recaptcha2`](https://platform.acedata.cloud/documents/b9a02028-d438-48b7-99b2-5b2eaf368bad?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/captcha/token/recaptcha3`](https://platform.acedata.cloud/documents/59b4b2ac-5264-4c8b-a5f1-102f893e7275?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
