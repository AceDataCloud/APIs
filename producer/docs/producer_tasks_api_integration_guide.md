# Producer Tasks API Integration and Usage

The main function of the Producer Tasks API is to query the execution status of tasks by inputting the task ID returned by the Producer Audios Generation API.

This document describes the Producer Tasks API integration, helping you query the status and final result of an asynchronous Producer music generation task.

## Application Process

To use the Producer Tasks API, you first need to apply for the corresponding service on the application page [Producer Audios Generation API](https://platform.acedata.cloud/documents/01d96900-9f8c-41d7-814c-95c7a885ba61), and then copy the task ID returned by the Producer Audios Generation API.

Finally, go to the Tasks API page [Producer Tasks API](https://platform.acedata.cloud/documents/e706d672-d7c9-4232-8652-0cf53219e7bf) to apply for the corresponding service. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Example

The Producer Tasks API queries the result of a task created by the Producer Audios Generation API. Create the task with `"async": true` (or a `callback_url`), then poll with the returned `id`.

### Request Body

- `id`: a single task ID returned by the Producer Audios Generation API.
- `ids`: optional array to query multiple tasks at once.
- `action`: optional operation type.

### Code Example

```bash
curl -X POST 'https://api.acedata.cloud/producer/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "id": "75d8e08f-b25f-450e-9496-7b52e393098b"
  }'
```

```python
import requests

url = "https://api.acedata.cloud/producer/tasks"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {"id": "75d8e08f-b25f-450e-9496-7b52e393098b"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

```json
{
  "data": [
    {
      "id": "75d8e08f-b25f-450e-9496-7b52e393098b",
      "state": "complete",
      "audio_url": "https://platform.cdn.acedata.cloud/producer/song.mp3",
      "video_url": "https://platform.cdn.acedata.cloud/producer/song.mp4",
      "title": "Song Title"
    }
  ]
}
```

Task records returned by `retrieve` / `retrieve_batch` include the following metadata fields:

- `created_at`: task creation time (Unix timestamp in seconds).
- `started_at`: task start execution time (ISO-8601 UTC string).
- `finished_at`: task completion time (Unix timestamp in seconds; omitted when unfinished).
- `elapsed`: task execution time in seconds (float; omitted when unfinished).

Only `state: "complete"` with `success: true` means the job is finished. While `state` is `pending`, the API may return an intermediate `audio_url` (streaming preview) — keep polling every 3–5 seconds until the state is complete.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
