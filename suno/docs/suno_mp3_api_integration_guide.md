# Suno MP3 URL API Integration Instructions

The Suno MP3 URL API creates a playable `.mp3` address for existing music. Use the `audio_id` returned by Suno audio generation. Each call creates an independent MP3 URL task without changing the original generation task or audio ID.

## Synchronous Call

```python
import requests

response = requests.post(
    "https://api.acedata.cloud/suno/mp3",
    headers={
        "accept": "application/json",
        "authorization": "******",
        "content-type": "application/json"
    },
    json={"audio_id": "ef1ec21e-1540-4eb6-8fa5-26cb8b90d28f"},
    timeout=240
)
response.raise_for_status()
result = response.json()
print(result["data"][0]["file_url"])
```

On success, `data[0].file_url` is the playable audio address. The platform prioritizes storing it at `https://cdn.acedata2.cloud/suno/{audio_id}.mp3`; if persistence fails, it returns the currently available original media address.

## Asynchronous Call

For longer processing, pass `async: true`:

```python
submission = requests.post(
    "https://api.acedata.cloud/suno/mp3",
    headers={"authorization": "******"},
    json={
        "audio_id": "ef1ec21e-1540-4eb6-8fa5-26cb8b90d28f",
        "async": True
    }
).json()

export_task_id = submission["task_id"]
```

Query `export_task_id` through `/suno/tasks`, or provide a `callback_url` for the final result. Synchronous responses, task queries, and callbacks use the same terminal data structure.

## Notes

- `audio_id` must identify recognizable Suno audio.
- MP3 URL tasks are independent of the original music generation task.
- Persistence failures do not block a result while the original media remains available.
- Download results promptly and retain them according to your data retention policy.
