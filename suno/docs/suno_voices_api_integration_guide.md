# Suno Voices API Integration Instructions

SUNO allows us to create a custom voice persona from any audio file, enabling voice cloning for music generation. Unlike the existing Persona API (which uses a Suno-generated `audio_id`), this API accepts a publicly accessible `audio_url` — your own vocal recording. This document explains the integration method for the voice cloning API.

## Step 1: Create a Voice Persona

This API has three input parameters: `audio_url` (required), a publicly accessible MP3 or WAV audio file URL containing clear vocals from a single speaker; and `name` and `description` (optional), for the name and description of the voice persona.

**Audio file requirements:**
- Format: MP3 or WAV
- Duration: at least 10 seconds
- Content: clear vocals from a single speaker, with minimal background noise or music

```bash
curl -X POST 'https://api.acedata.cloud/suno/voices' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "audio_url": "http://cos.aitutu.cc/mp4/ru-user-voice.mp3",
  "name": "RU User Voice Test",
  "description": "用户语音录音示例"
}'
```

The result is as follows:

```json
{
  "success": true,
  "task_id": "b9150e51-d87c-4556-a55e-100947a63bdf",
  "data": {
    "persona_id": "e95013f8-eaee-4741-a42f-1d559a9d0b2b",
    "name": "RU User Voice Test",
    "is_public": false
  }
}
```

As can be seen, the `persona_id` field in `data` is the ID of the created voice persona. `is_public` is always `false` because voice personas created from uploaded audio are private.

## Step 2: Generate Music Using the Voice Persona

With the voice persona ID, we can use the [Suno Audios Generation API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9) to generate music. Set `action` to `generate` and `persona_id` to the voice persona ID returned above — the generated song will be sung in the cloned voice.

> **Note:** Voice cloning only supports `chirp-v4-5` and above (e.g., `chirp-v4-5`, `chirp-v5`, `chirp-v5-5`). It does not support `chirp-v4`.

```bash
curl -X POST 'https://api.acedata.cloud/suno/audios' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "generate",
  "model": "chirp-v5-5",
  "prompt": "A warm synth-pop song about city nights",
  "persona_id": "e95013f8-eaee-4741-a42f-1d559a9d0b2b"
}'
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

As can be seen, the generated song uses the cloned voice. The `persona_id` can also be used with the `cover` action to cover existing songs in the cloned voice.
