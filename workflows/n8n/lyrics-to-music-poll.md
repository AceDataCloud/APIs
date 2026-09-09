# Lyrics to music with bounded polling

[`lyrics-to-music-poll.json`](lyrics-to-music-poll.json) generates lyrics from a theme, submits those lyrics as a custom asynchronous song request, polls the resulting task, and returns one structured track. It uses only built-in n8n nodes and caps music polling at 20 attempts separated by 15 seconds.

Last contract verification: **2026-09-10**.

## Import and setup

1. Download `lyrics-to-music-poll.json`.
2. In n8n, choose **Import from File**. For CLI validation, run `n8n import:workflow --input=lyrics-to-music-poll.json` against an isolated n8n user folder/database first.
3. The stable template ID is `acedata-lyrics-to-music-poll-v1`. An n8n CLI import can overwrite an existing workflow with the same ID; change or remove the ID before importing if you need a separate copy.
4. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-lyrics-to-music-poll).
5. Create one **Header Auth** credential:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
6. Select that credential separately in **Generate lyrics with Ace Data Cloud**, **Submit music with Ace Data Cloud**, and **Poll music task**.
7. Edit `theme`, `style`, `lyrics_model`, or `music_model` in **Set song input**, then run the workflow.

The exported workflow contains no credential ID, token, pinned response, or user data. n8n stores credential data separately from the workflow JSON.

## Inputs and request chain

| Field | Default | Contract |
| --- | --- | --- |
| `theme` | Hopeful city-garden song | Prompt sent to lyrics generation |
| `style` | Warm indie folk | Style sent to custom music generation |
| `lyrics_model` | `default` | Must be `default` or `remi-v1` |
| `music_model` | `chirp-v5-5` | Must remain in the music endpoint model enum |

The first request sends `prompt + model` to `POST https://api.acedata.cloud/suno/lyrics`. It must return HTTP 200, `success=true`, and a first candidate with non-empty `text` and `title` before music generation begins.

The second request sends that candidate to `POST https://api.acedata.cloud/suno/audios` with:

```json
{
  "action": "generate",
  "model": "chirp-v5-5",
  "custom": true,
  "lyric": "<generated lyrics>",
  "title": "<generated title>",
  "style": "warm indie folk, acoustic guitar, gentle percussion",
  "instrumental": false,
  "async": true
}
```

Keep the fixed action and custom-mode fields as exported unless you have checked the current endpoint schema. The workflow uses the first generated lyrics candidate; review or select among candidates before the music request if your use case requires editorial control.

## Polling and failure behavior

The music submit response must have HTTP 200 and a non-empty `task_id`. The workflow then creates exactly 20 poll items. For each item it waits 15 seconds and calls `POST https://api.acedata.cloud/suno/tasks` with `action=retrieve` and the music task ID.

The workflow does not infer undocumented task status strings:

- no numeric `finished_at`: continue to the next bounded attempt;
- numeric `finished_at` plus `response.success=true`, a non-empty result array, and a non-empty first `audio_url`: return success;
- numeric `finished_at` without that result contract: stop as a terminal failure;
- all 20 attempts consumed: stop with a timeout error.

Every HTTP response must be exactly 200. Lyrics transport/API failures, missing lyrics, music submit failures, a missing music task ID, poll failures, terminal task failures, and polling timeout all stop explicitly with response context. The lyrics timeout is 120 seconds; music submit and poll timeouts are each 60 seconds. The scheduled music polling window is approximately five minutes, excluding request latency.

A successful run returns the first usable track:

```json
{
  "status": "success",
  "lyrics_task_id": "...",
  "music_task_id": "...",
  "model": "chirp-v5-5",
  "title": "...",
  "style": "...",
  "lyrics": "[Verse]...",
  "audio_id": "...",
  "audio_url": "https://...",
  "image_url": "https://...",
  "duration_seconds": 154.9,
  "elapsed_seconds": 92.4
}
```

Music generation can return more than one candidate. This template emits the first candidate with a validated audio URL; the full task response remains in the n8n execution record.

## Cost and data boundary

- A complete execution makes **one billable lyrics-generation request and one billable music-generation request**, plus up to 20 task-retrieval requests. Failed, timed-out, or manually retried executions can add requests. Check current pricing before activation.
- The theme is sent for lyrics generation. The selected lyrics/title, style, model, and generation options are then sent for music generation. Task IDs, generated text, task records, and media URLs are present in n8n execution data.
- n8n executions can remain stored according to the instance's retention settings. Configure retention before processing sensitive material.
- Do not send secrets, personal data, copyrighted lyrics you cannot use, or content you are not authorized to process. Review generated lyrics and music for accuracy, rights, and policy compliance before publication.
