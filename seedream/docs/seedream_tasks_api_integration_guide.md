# Seedream Tasks API Integration and Usage

The Seedream Tasks API queries the execution status of an async task created by the Seedream Images Generation API.

## Get an API key

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Keep the key on your server and use it in place of `{token}` in the examples.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

API reference: [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75), [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e).

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{ "id": "ec22ae22-0140-4033-8c86-a48b536da595" }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "data": { "status": "succeeded", "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png", "model": "doubao-seedream-5-0-lite-260128" }
}
```

Poll until `data.status` is `succeeded`, then download `data.image_url`.

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | bad_request | Missing/invalid task id |
| 401 | invalid_token | Token bad |
| 404 | not_found | Task id not found |
