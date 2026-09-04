# Suno Voices API Integration Instructions

Suno allows you to create a custom voice persona from your own audio recording. The resulting `persona_id` can then be used with the [Suno Audios Generation API](https://platform.acedata.cloud/documents/suno-audios) to generate songs in that voice.

This API accepts three parameters:

- `audio_url`: A publicly accessible URL of an MP3 or WAV file, 10–240 seconds long, containing a clear single voice. Clean 30–60 second speech or singing clips work best; avoid background noise, accompaniment, echo, reverb, and multiple speakers.
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

With the voice persona ID, you can use the [Suno Audios Generation API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9) to generate songs in that voice. Pass `action` as `artist_consistency` (or `artist_consistency_vox` for Persona-v2-vox) and include the `persona_id` returned above.

Voice personas created from uploaded audio are private and cannot be reused across accounts. Voice cloning can occasionally return `voices_sound_different` even for compliant audio; retrying the same material usually succeeds. Implement one or two automatic retries for failed results—failed requests are not charged.

## Generate Music with a Voice Persona

Use `action: "generate"` and the returned `persona_id` to generate music with the cloned voice. Voice cloning requires `chirp-v4-5` or later models.

```bash
curl -X POST 'https://api.acedata.cloud/suno/audios' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "action": "generate",
    "model": "chirp-v5-5",
    "prompt": "A warm synth-pop song about city nights",
    "persona_id": "dde0be60-5280-4bd2-89a0-4020ddd3db52"
  }'
```

The corresponding Python code:

```python
import requests

url = "https://api.acedata.cloud/suno/voices"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "audio_url": "https://cdn.acedata.cloud/suno_demo.mp3",
    "name": "My Voice",
    "description": "A clear male vocal recorded in a quiet room"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```
