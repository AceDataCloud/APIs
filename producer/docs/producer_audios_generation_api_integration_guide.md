# Producer Audios Generation API Integration Instructions

This article introduces the Producer Audios Generation API integration instructions, which generate AI songs from a text prompt or custom lyrics, with support for instrumental tracks, covers, extensions, and section replacement.

## Application Process

To use the Producer Audios Generation API, apply for the corresponding service on the [Producer Audios Generation API](https://platform.acedata.cloud/documents/01d96900-9f8c-41d7-814c-95c7a885ba61) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to input an `action` plus a `prompt`. The request body fields are described below:

- `action`: the operation type. `generate` (new song), `cover`, `extend`, `replace_section`.
- `prompt`: the song description used when `custom` is false.
- `model`: the model used to generate the song (e.g. `FUZZ-2.0 Pro`). Defaults to the highest-quality model.
- `custom`: enable custom lyrics mode (`true` / `false`).
- `lyric`: custom lyrics with `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]` tags.
- `title`: song title.
- `instrumental`: produce a pure instrumental track with no vocals.
- `audio_id`: an existing audio ID, required for `extend` / `cover` / `replace_section`.
- `continue_at`: extension start point, in seconds.
- `replace_section_start` / `replace_section_end`: time range to regenerate, in seconds.
- `lyrics_strength`, `sound_strength`, `weirdness`: 0–1 creative controls.
- `seed`: seed for reproducibility.
- `callback_url`: an asynchronous callback URL. When provided, the API returns immediately with a `task_id` and POSTs the result when generation completes.
- `async`: optional. When `true`, the API returns immediately with a `task_id`; poll the result with the Producer Tasks API.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/producer/audios' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "action": "generate",
    "prompt": "chill lo-fi hip hop with rain sounds and soft piano"
  }'
```

### Response Example

```json
{
  "data": [
    {
      "id": "75d8e08f-b25f-450e-9496-7b52e393098b",
      "lyric": "[Verse]\nSleigh bells ringin', choirs singin'\n...",
      "audio_url": "https://platform.cdn.acedata.cloud/producer/song.mp3",
      "video_url": "https://platform.cdn.acedata.cloud/producer/song.mp4",
      "image_url": "https://platform.cdn.acedata.cloud/producer/cover.jpg",
      "title": "Song Title",
      "style": "electronic, dance",
      "model": "FUZZ-2.0 Pro"
    }
  ]
}
```

The returned `data` array contains each generated track's `id`, `audio_url`, `video_url`, `image_url`, `title`, `lyric`, `style`, and `model`.

## Workflows

### Generate from a Prompt

Send `action: "generate"` with a `prompt` (see the request example above).

### Custom Lyrics Mode

```json
{
  "action": "generate",
  "custom": true,
  "title": "Midnight City",
  "lyric": "[Verse]\nNeon lights reflect on wet streets\n[Chorus]\nMidnight city never sleeps",
  "instrumental": false
}
```

### Extend a Song

```json
{ "action": "extend", "audio_id": "existing-audio-id", "continue_at": 30 }
```

### Replace a Section

```json
{ "action": "replace_section", "audio_id": "existing-audio-id", "replace_section_start": 15, "replace_section_end": 30 }
```

## Related Endpoints

- `POST /producer/lyrics` — draft lyrics from a `prompt`.
- `POST /producer/wav` / `POST /producer/videos` — export a finished `audio_id` to WAV / MP4.
- `POST /producer/upload` — register a reference `audio_url` for cover/extend.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
