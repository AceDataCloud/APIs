# Fish TTS API Integration Instructions

This article introduces the Fish TTS API integration instructions, which converts text into natural speech and can optionally use a custom cloned voice model.

## Application Process

To use the Fish TTS API, apply for the corresponding service on the [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to input `text`. The result is a synthesized audio file. The request body fields are described below:

- `text`: the text to synthesize into speech (required).
- `reference_id`: the voice model ID (or IDs) to use for the timbre. Create one with the Fish Model Create API.
- `references`: inline reference samples.
- `format`: output audio format: `mp3`, `wav`, or `pcm`. Both `wav` and `pcm` return a WAV container.
- `sample_rate`: output sample rate.
- `mp3_bitrate`: MP3 bitrate: `64`, `128`, or `192`.
- `latency`: latency mode (`normal` / `balanced`).
- `chunk_length` / `min_chunk_length`: chunk sizing for streaming.
- `temperature`, `top_p`, `repetition_penalty`, `max_new_tokens`: generation controls.
- `normalize`: whether to normalize text before synthesis.
- `prosody`: prosody controls.
- `callback_url`: an asynchronous callback URL.
- `async`: optional asynchronous mode.

> The TTS engine is selected with the **`model` request header** — not a body field.
> Supported values are `s1`, `s2-pro` (default), and `s2.1-pro`. `s2.1-pro` is the latest
> generation and `s2-pro` is the most expressive, while `s1` is steadier on long passages.
> All three are priced the same.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "text": "The quick brown fox jumps over the lazy dog.",
    "format": "mp3"
  }'
```

### Response Example

```json
{
  "audio_url": "https://platform2.cdn.acedata.cloud/fish/8a72ff98-4023-4006-a9f7-4cb2fa04f978.mp3"
}
```

Download the generated audio from the `audio_url` field.
The response can also include `cost` with `amount`, `currency`, and `list_amount`.

## Workflows

### Synthesize with a Cloned Voice

First create a voice model with the Fish Model Create API (`POST /fish/model`) to obtain a model ID, then pass it as `reference_id`:

```json
{
  "text": "Welcome to our platform.",
  "reference_id": "d7900c21663f485ab63ebdb7e5905036"
}
```

## Gotchas

- Pricing is based on the byte count of the generated audio.
- Voice cloning requires a clear reference audio sample.
- With `callback_url`, the immediate response contains `task_id` and `started_at`; the callback receives `task_id` and `audio_url`.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
