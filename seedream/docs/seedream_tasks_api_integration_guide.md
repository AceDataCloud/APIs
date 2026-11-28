# Seedream Tasks API Integration and Usage

The Seedream Tasks API queries the execution status of an async task created by the Seedream Images Generation API.

## Application Process

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Initialize it on your first visit if prompted, then copy the key shown in **API KEY**. Keep the copied key on your server and use it in place of `{token}` below.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

To call the [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75), copy the task ID returned by the [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) (submit with `"async": true`).

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
