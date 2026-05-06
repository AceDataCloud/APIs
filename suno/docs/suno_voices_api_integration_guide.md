# Suno Voices API Integration Instructions

Suno allows you to create a custom voice persona from your own audio recording. The resulting `persona_id` can then be used with the [Suno Audios Generation API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9) to generate songs in that voice.

This API accepts three parameters:

- `audio_url`: A publicly accessible URL of the audio file (MP3 or WAV format, at least 10 seconds long, containing clear vocals from a single speaker without background noise or music).
- `name`: The name for the custom voice persona.
- `description`: A description of the custom voice persona.

```bash
curl -X POST 'https://api.acedata.cloud/suno/voices' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "audio_url": "https://cdn.acedata.cloud/suno_demo.mp3",
  "name": "My Voice",
  "description": "A clear male vocal recorded in a quiet room"
}'
```

The result is as follows:

```json
{
  "success": true,
  "task_id": "8e808558-f056-456f-91d6-b97fd94eb3be",
  "data": {
    "persona_id": "dde0be60-5280-4bd2-89a0-4020ddd3db52",
    "name": "My Voice",
    "is_public": false
  }
}
```

As can be seen, the `persona_id` field in `data` is the ID of the created voice persona. Voice personas created from uploaded audio are always private (`is_public: false`).

With the voice persona ID, you can use the [Suno Audios Generation API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9) to generate songs in that voice. Set `action` to `generate` and pass the `persona_id` returned above.

> **Note:** Voice cloning only supports `chirp-v4-5` and above (e.g. `chirp-v4-5`, `chirp-v5`, `chirp-v5-5`). It does **not** support `chirp-v4`.

```python
import requests

url = "https://api.acedata.cloud/suno/audios"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "action": "generate",
    "model": "chirp-v5-5",
    "prompt": "A warm synth-pop song about city nights",
    "persona_id": "e95013f8-eaee-4741-a42f-1d559a9d0b2b"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The result is as follows:

```json
{
  "success": true,
  "task_id": "53d8a334-a972-43c5-895e-60c4454e88d5",
  "data": [
    {
      "id": "16463960-077c-4700-bbb3-3c7897b943d3",
      "title": "Soft Neon on My Skin",
      "audio_url": "https://cdn1.suno.ai/16463960-077c-4700-bbb3-3c7897b943d3.mp3",
      "image_url": "https://cdn2.suno.ai/image_16463960-077c-4700-bbb3-3c7897b943d3.jpeg",
      "model": "chirp-v5-5",
      "state": "succeeded",
      "prompt": "A warm synth-pop song about city nights",
      "duration": 156.28
    }
  ]
}
```

The generated song uses the cloned voice. The `persona_id` can also be used with the `cover` action to cover an existing song in the cloned voice.
