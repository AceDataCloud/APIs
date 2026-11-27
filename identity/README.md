# Identity Authentication API

Validate identity information and extract document fields through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/identity/identity_idcard_check-1e) · [Models and pricing](https://platform.acedata.cloud/services/a0a76008-85ff-4c46-8db7-76481721b9fb?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/identity/identity_idcard_check-1e)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Replace `image_url` with an accessible image of the identity document for the verification you are authorized to perform. The response contains document fields. Avoid writing these fields to application logs.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/identity/idcard/check-1e \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "image_url": "https://YOUR_DOCUMENT_IMAGE"
}'
```

Read `id_num` from the response. The following fields illustrate a successful result.

```json
{
  "id_num": "DOCUMENT_NUMBER"
}
```

## API reference

- [`/identity/bankcard/check-1e`](https://platform.acedata.cloud/documents/5c98d0d5-729e-47e1-9719-d22b6b4efaf4?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-2e`](https://platform.acedata.cloud/documents/6e3c7e69-632f-4e59-b0bc-c0363ffe1c1f?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-3e`](https://platform.acedata.cloud/documents/3a0d976c-69e9-4995-a249-91738d103c11?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-4e`](https://platform.acedata.cloud/documents/efd09245-9092-426a-b721-9145a3c06e87?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/check-1e`](https://platform.acedata.cloud/documents/10455fc1-2399-40b4-b486-4a93812b4143?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/check-2e`](https://platform.acedata.cloud/documents/78e1cf92-2bde-4599-ac4c-75485130e548?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/ocr`](https://platform.acedata.cloud/documents/5eb27329-8f0b-4e02-b8cc-54c7ba96633d?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-1e`](https://platform.acedata.cloud/documents/e90adc40-95f0-418a-8fd5-6dec725a9f4f?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-2e`](https://platform.acedata.cloud/documents/34c42afe-f2ce-423f-8e19-dcf1ba650346?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-3e`](https://platform.acedata.cloud/documents/f34e4918-4aaf-4a21-b007-25636b37cf2f?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
