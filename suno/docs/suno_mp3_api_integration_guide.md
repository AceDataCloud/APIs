# Suno MP3 URL API Integration Guide

The Suno MP3 URL API generates a playable `.mp3` URL for existing music. Use it when an old download URL is unavailable, mobile playback is required, or a public audio URL must be retrieved again.

## Request

`audio_id` is required and must be an audio ID returned by the Suno audio generation API. Each request creates an independent MP3 URL task and does not modify the source audio.

```python
import requests

response = requests.post(
    "https://api.acedata.cloud/suno/mp3",
    headers={
        "accept": "application/json",
        "authorization": "******",
        "content-type": "application/json",
    },
    json={"audio_id": "ef1ec21e-1540-4eb6-8fa5-26cb8b90d28f"},
    timeout=240,
)
response.raise_for_status()
result = response.json()
print(result["data"][0]["file_url"])
```

On success, `data[0].file_url` is the playable URL. The service prioritizes `https://platform2.cdn.acedata.cloud/suno/{audio_id}.mp3`; if transfer takes longer than 30 seconds or fails, it returns the currently available source audio URL.

## Asynchronous Request

Set `async` to `true` for longer processing. Optionally provide `callback_url` to receive the final result.

```python
submission = requests.post(
    "https://api.acedata.cloud/suno/mp3",
    headers={"authorization": "******"},
    json={
        "audio_id": "ef1ec21e-1540-4eb6-8fa5-26cb8b90d28f",
        "async": True,
    },
).json()

export_task_id = submission["task_id"]
```

Query `export_task_id` through `/suno/tasks`. Synchronous responses, task queries, and callbacks use the same terminal data structure.
