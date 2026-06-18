# Suno MIDI Generation API Integration Instructions

Suno allows us to create secondary works from generated music and obtain the MIDI of the music. This document explains the integration methods for the related API.

The core input parameter for this API is `audio_id`, which is the official song ID generated, typically corresponding to the full track separated song ID (where the parameter `action` is `all_stems` in [song generation](https://platform.acedata.cloud/documents/suno-audios)). Optionally, it also supports `callback_url` for asynchronous callback addresses.

The `audio_id` we input here is `c65e6ffd-ead3-4926-9c8c-a42ce202946b`.

```python
import requests

url = "https://api.acedata.cloud/suno/midi"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "audio_id": "c65e6ffd-ead3-4926-9c8c-a42ce202946b"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The result is as follows:

```json
{
  "success": true,
  "task_id": "4f94486d-5013-4bcc-922f-39bd52b5cd4a",
  "trace_id": "8bc8cca3-2d4b-46d0-a4fa-bb355af9902c",
  "data": [
    {
      "file_url": "https://cdn1.suno.ai/c65e6ffd-ead3-4926-9c8c-a42ce202946b.mid"
    }
  ]
}
```

As we can see, the `file_url` field in `data` is the URL to the MIDI file of the generated music.
