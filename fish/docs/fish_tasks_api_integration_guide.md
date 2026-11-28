# Fish Tasks API Integration and Usage

The main function of the Fish Tasks API is to query the execution status of tasks by inputting the task ID returned by the Fish TTS API.

This document describes the Fish Tasks API integration, helping you query the status and final result of an asynchronous Fish voice generation task.

## Application Process

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Copy the key shown in **API KEY**. Keep the copied key on your server and use it in place of `{token}` below.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

Copy the task ID returned by [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d).

Use that ID to query the [Fish Tasks API](https://platform.acedata.cloud/documents/fc541fac-a941-47fd-b6f7-48d6cb9da523).

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Example

The Fish Tasks API queries the result of a task created by the Fish TTS API. Create the task with `"async": true` (or a `callback_url`), then poll with the returned `id`.

### Request Body

- `id`: a single task ID returned by the Fish TTS API.
- `ids`: optional array to query multiple tasks at once.
- `action`: optional operation type.

### Code Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978"
  }'
```

```python
import requests

url = "https://api.acedata.cloud/fish/tasks"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {"id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

```json
{
  "data": {
    "task_id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978",
    "status": "succeeded",
    "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
  },
  "success": true
}
```

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [platform documentation](https://platform.acedata.cloud/documents?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
