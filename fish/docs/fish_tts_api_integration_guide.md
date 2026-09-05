# Fish TTS API Integration Instructions

This article introduces the Fish TTS API integration instructions, which converts text into natural speech and can optionally use a custom cloned voice model.

## Application Process

To use the Fish TTS API, apply for the corresponding service on the [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to input `text`. The result is a synthesized audio file. The request body fields are described below:

- `text`: the text to synthesize into speech (required).
- `reference_id`: the voice model ID (or an array of IDs) to use for the timbre. Create IDs with the Fish Model Create API.
- `format`: output audio format: `mp3`, `wav`, or `pcm`.
- `sample_rate`: output sample rate.
- `mp3_bitrate`: MP3 encoding bitrate.
- `latency`: latency mode (`normal` / `balanced`).
- `chunk_length` / `min_chunk_length`: chunk sizing for streaming.
- `temperature`, `top_p`, `repetition_penalty`, `max_new_tokens`: generation controls.
- `normalize`: whether to normalize text before synthesis.
- `prosody`: prosody controls.
- `references`: one one-shot clone sample (exactly one item) containing `audio` (public HTTPS MP3/WAV URL) and `text` (exact transcript). Do not combine with `reference_id`.
- `callback_url`: an asynchronous callback URL.
- `async`: optional. When `true`, the API returns immediately with a `task_id`; poll the result with the Fish Tasks API.

> The TTS engine is selected with the **`model` request header** — not a body field.
> Supported values are `s1`, `s2-pro` (default) and `s2.1-pro`. `s2.1-pro` is the latest
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
  "audio_url": "https://platform2.cdn.acedata.cloud/fish/995dfe37-b187-474d-8323-b08d6678ed8f.mp3"
}
```

Download the generated audio from the `audio_url` field.

## Workflows

### Synthesize with a Cloned Voice

First create a voice model with the Fish Model Create API (`POST /fish/model`) to obtain a model ID, then pass it as `reference_id`:

```json
{
  "text": "Welcome to our platform.",
  "reference_id": "d7900c21663f485ab63ebdb7e5905036"
}
```

### One-shot Voice Clone

Use a reference voice for one request without creating a persistent model:

```json
{
  "text": "New speech in the referenced voice.",
  "format": "mp3",
  "references": [{
    "audio": "https://cdn.acedata.cloud/reference.mp3",
    "text": "The exact words spoken in the reference audio."
  }]
}
```

Use one public HTTPS MP3/WAV reference lasting 10–270 seconds. Raw bytes, Base64, data URIs, and MessagePack are not accepted by this endpoint. Use `reference_id` instead when reusing a saved/public voice.

## Gotchas

- Pricing is based on the UTF-8 byte count of the target input text, not the generated audio size.
- Voice cloning requires a clear reference audio sample.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
