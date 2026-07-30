# Fish TTS API Integration Instructions

This article introduces the Fish TTS API integration instructions, which convert text into natural speech and optionally use a cloned voice model while keeping the upstream Fish request body format.

## Application Process

To use the Fish TTS API, apply for the corresponding service on the [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to input `text`. The result is a synthesized audio file. The request body fields are described below:

- `text`: the text to synthesize into speech (required).
- `format`: output audio format. Supported values are `mp3` (default), `wav`, and `pcm`. `wav` and `pcm` both return WAV containers; `opus` is not supported.
- `reference_id`: one voice model ID, or an array of voice model IDs, to use for the timbre. Create them with the Fish Model APIs.
- `references`: inline reference samples. Use this instead of `reference_id` when you want to send audio/text examples directly in the request.
- `sample_rate`: output sample rate, such as `16000`, `22050`, or `44100`.
- `mp3_bitrate`: MP3 bitrate. This field is used only when `format` is `mp3`.
- `prosody`: prosody overrides, including `speed` and `volume`.
- `chunk_length`: upstream chunk sizing parameter.
- `temperature` and `top_p`: generation controls.
- `latency`: latency mode (`normal` or `balanced`). When omitted, Ace Data Cloud fills in `normal`.
- `normalize`: whether to normalize text before synthesis.
- `callback_url`: an asynchronous callback URL. This is an Ace Data Cloud extension beyond the upstream Fish API.

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
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

Download the generated audio from the `audio_url` field. When you submit `callback_url`, the API returns a `task_id` immediately and later POSTs the final result to your callback URL; you can also query it with the Fish Tasks API.

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

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
