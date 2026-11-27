# Identity Authentication API

Validate identity information and extract document fields through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/identity-idcard-check-1e-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/a0a76008-85ff-4c46-8db7-76481721b9fb?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/identity-idcard-check-1e-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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

Replace `image_url` with an accessible image of the identity document for the verification you are authorized to perform. The response contains document fields. Avoid writing these fields to application logs.

### Request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/identity/idcard/check-1e \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "image_url": "https://YOUR_DOCUMENT_IMAGE"
}'
```

### Response JSON

Illustrative response with placeholder identifiers and output values.

```json
{
  "result": "RESULT_CODE",
  "description": "VERIFICATION_DESCRIPTION",
  "name": "DOCUMENT_NAME",
  "id_num": "DOCUMENT_NUMBER",
  "sex": "DOCUMENT_SEX",
  "birth": "DOCUMENT_BIRTH_DATE",
  "address": "DOCUMENT_ADDRESS"
}
```

Check `result` and `description` for the verification outcome. The remaining fields contain document data from your request.

## API reference

- [`/identity/bankcard/check-1e`](https://platform.acedata.cloud/documents/identity-bankcard-check-1e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-2e`](https://platform.acedata.cloud/documents/identity-bankcard-check-2e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-3e`](https://platform.acedata.cloud/documents/identity-bankcard-check-3e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/bankcard/check-4e`](https://platform.acedata.cloud/documents/identity-bankcard-check-4e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/check-1e`](https://platform.acedata.cloud/documents/identity-idcard-check-1e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/check-2e`](https://platform.acedata.cloud/documents/identity-idcard-check-2e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/idcard/ocr`](https://platform.acedata.cloud/documents/identity-idcard-ocr?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-1e`](https://platform.acedata.cloud/documents/identity-phone-check-1e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-2e`](https://platform.acedata.cloud/documents/identity-phone-check-2e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/identity/phone/check-3e`](https://platform.acedata.cloud/documents/identity-phone-check-3e?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
