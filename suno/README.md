# Suno API

Create songs from a short description or your own lyrics through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/suno-audios-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/suno?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/suno-audios-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. If needed, select **Initialize General Application** first. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

### Submit a request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/suno/audios \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "generate",
  "model": "chirp-v6",
  "custom": false,
  "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
  "async": true
}'
```

### Submission response JSON

The following JSON examples illustrate the documented fields. IDs, timestamps and output URLs are placeholders. Use the values returned by your own request.

```json
{
  "task_id": "TASK_ID"
}
```

Save `task_id` and query that same task.

### Query the task

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/suno/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"TASK_ID"}'
```

### Processing response JSON

```json
{
  "id": "TASK_ID",
  "type": "audios",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "chirp-v6",
    "custom": false,
    "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
    "async": true
  },
  "finished_at": null
}
```

Query again after a few seconds while processing continues.

### Completed response JSON

```json
{
  "id": "TASK_ID",
  "type": "audios",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "chirp-v6",
    "custom": false,
    "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
    "async": true
  },
  "finished_at": 1790000045,
  "elapsed": 45,
  "response": {
    "success": true,
    "task_id": "TASK_ID",
    "trace_id": "TRACE_ID",
    "data": [
      {
        "id": "AUDIO_ID_1",
        "model": "chirp-v6",
        "state": "succeeded",
        "title": "A New Beginning",
        "audio_url": "https://media.example.com/song-1.mp3"
      },
      {
        "id": "AUDIO_ID_2",
        "model": "chirp-v6",
        "state": "succeeded",
        "title": "A New Beginning",
        "audio_url": "https://media.example.com/song-2.mp3"
      }
    ]
  }
}
```

Continue while `finished_at` is null or absent. When the task finishes, inspect `response.success` and the result state. On success, open `response.data[*].audio_url`. On failure, inspect `response.error` and retain the original task ID for support.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

## APIs and Guides

Explore the supported endpoints and integration guides for Suno Music Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Suno Audios Generation API](https://platform.acedata.cloud/documents/suno-audios?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/audios` | [Suno Audios Generation API Integration Guide](https://platform.acedata.cloud/documents/suno-audios-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Persona API](https://platform.acedata.cloud/documents/suno-persona?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/persona` | [Suno Persona API Integration Guide](https://platform.acedata.cloud/documents/suno-persona-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno MP4 API](https://platform.acedata.cloud/documents/suno-mp4?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/mp4` | [Suno MP4 API Integration Guide](https://platform.acedata.cloud/documents/suno-mp4-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Vox API](https://platform.acedata.cloud/documents/suno-vox?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/vox` | [Suno Vox API Integration Guide](https://platform.acedata.cloud/documents/suno-vox-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [$t(document_title_suno_timing_generation_api)](https://platform.acedata.cloud/documents/suno-timing?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/timing` | [Suno Timing API Integration Guide](https://platform.acedata.cloud/documents/suno-timing-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Wav API](https://platform.acedata.cloud/documents/suno-wav?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/wav` | [Suno Wav API Integration Guide](https://platform.acedata.cloud/documents/suno-wav-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno MIDI API](https://platform.acedata.cloud/documents/suno-midi?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/midi` | [Suno MIDI API Integration Guide](https://platform.acedata.cloud/documents/suno-midi-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Style Generation API](https://platform.acedata.cloud/documents/suno-style?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/style` | [Suno Style API Integration Guide](https://platform.acedata.cloud/documents/suno-style-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Lyrics Generation API](https://platform.acedata.cloud/documents/suno-lyrics?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/lyrics` | [Suno Lyrics Generation API Integration Guide](https://platform.acedata.cloud/documents/suno-lyrics-generation-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno MashupLyrics Generation API](https://platform.acedata.cloud/documents/suno-mashup-lyrics?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/mashup-lyrics` | [Suno Mashup Lyrics Generation API Integration Guide](https://platform.acedata.cloud/documents/suno-mashup-lyrics-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Tasks API](https://platform.acedata.cloud/documents/suno-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/tasks` | [Suno Tasks API Integration Guide](https://platform.acedata.cloud/documents/suno-tasks-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Upload API](https://platform.acedata.cloud/documents/suno-upload?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/upload` | [Suno Upload API Integration Guide](https://platform.acedata.cloud/documents/suno-upload-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Suno Audio Availability Check API (Beta)](https://platform.acedata.cloud/documents/suno-availability?utm_source=github) | `/suno/availability` | [Audio availability precheck](docs/suno_audios_generation_api_integration_guide.md#audio-availability-precheck-beta) |
| [Suno Studio Projects API (Beta)](https://platform.acedata.cloud/documents/suno-projects?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/suno/projects` | [Project workflow](#studio-projects-beta) |

## MP3 export

Use `POST /suno/mp3` with the completed song's `audio_id`. Set `async=true` to receive a task ID and poll `/suno/tasks`; use the final returned `audio_url`. See the [MP3 integration guide](https://platform.acedata.cloud/documents/suno-mp3-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

Suno AI music and lyrics generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

![Suno Music Generation](https://cdn.acedata.cloud/20240403-192358.png/thumb_600x300)

API home page: [Ace Data Cloud - Suno Music Generation](https://platform.acedata.cloud/services/f2b646d8-3cfd-46ef-969a-1ea9eebde329?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

Keywords: suno-api, ai-music, music-generation, lyrics-generation, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Audio generation and processing

For `POST /suno/audios`, `negative_tags` excludes styles or genres only when `custom` is `true`. The API currently sets no fixed character limit for this field, but overly long content may still fail to process; keep it concise.

A downloadable audio file does not guarantee that its `audio_id` remains available for follow-up operations such as covers, extensions or stem separation. If `suno_processing_unavailable`, `suno_model_unavailable` or `suno_processing_failed` is returned, retain the `task_id` and `trace_id` and contact support. See the [audio generation integration guide](docs/suno_audios_generation_api_integration_guide.md) for the documented error messages.

### Replace a song section

For `/suno/audios` with `action: "replace_section"`, send the selected interval's local new lyrics in `lyric` and preferably the same text in `prompt`, not the entire song's lyrics. The default `full_song` mode returns two complete songs without another `concat` call; it does not guarantee unchanged duration or verbatim singing. Listen to the results before another edit, then use the chosen complete song's ID and recheck its timing. Follow the [replacement procedure](docs/suno_audios_generation_api_integration_guide.md#replace-section), not the separate Studio Projects procedure below.

### Standard request fees

| Operation | Credits per successful request |
| --- | --- |
| `/suno/lyrics` generation | 0.08, including multiple lyric candidates |
| `/suno/voices` creation | 0.15 |
| `/suno/audios` with `action: "stems"` | 0.56, including both vocal and instrumental outputs |

Failed requests are not charged; applicable discounts follow the actual bill. `all_stems` and `extract_stem` retain their own prices. See the [lyrics](docs/suno_lyrics_generation_api_integration_guide.md), [voices](docs/suno_voices_api_integration_guide.md), and [stem separation](docs/suno_audios_generation_api_integration_guide.md#vocal-and-instrument-separation) guides.

### Covers with a private voice

For a voice created through `/suno/voices`, first upload the original song to `/suno/upload` with `mode: "standard"` and the voice's `persona_id`. Then call `/suno/audios` with `action: "upload_cover"`, the returned `data.audio_id`, and the same `persona_id`. All three steps must use the same service channel. Do not reuse an audio ID uploaded without that voice association or combine `persona_id` with enhanced upload mode. `vocal_gender` is not required and cannot replace the voice ID. Follow the [private-voice cover procedure](docs/suno_voices_api_integration_guide.md#cover-a-song-with-a-private-voice).

### Audio availability check (Beta)

Before an extension or cover, optionally call `POST /suno/availability` with the completed song's UUID as `audio_id`, not its `task_id`. The check requires a Bearer API token, returns synchronously, and currently consumes no Credits. A successful check returns `data.id` and `data.available: true`, meaning positive evidence of availability on the current channel—not a guarantee that the next operation will succeed. If availability cannot be confirmed, `503 availability_unknown` is returned instead of `false`; other errors are not negative availability results either. See the [precheck procedure and error handling](docs/suno_audios_generation_api_integration_guide.md#audio-availability-precheck-beta).

### Persona management

`GET /suno/persona` listing and `DELETE /suno/persona` deletion consume no Credits, with no extra billing-exemption header required. Bearer API authentication is still required; `POST /suno/persona` creation continues to follow the API's existing pricing rules. See the [persona integration guide](docs/suno_persona_api_integration_guide.md).

## Custom Models (Beta)

Create a reusable music model from 6–24 authorized audio files, query its status, and generate new tracks through `POST /suno/custom-models`. See the [custom models integration guide](docs/suno_custom_models_api_integration_guide.md).

## Studio Projects (Beta)

Use `POST /suno/projects` to manage versioned multitrack projects. The [public API reference](https://platform.acedata.cloud/documents/suno-projects?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and [integration guide](https://platform.acedata.cloud/documents/suno-projects-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) contain the complete schema and recorded examples.

Send `Authorization: Bearer YOUR_API_KEY`, `Content-Type: application/json`, and an `Idempotency-Key` of 1–128 characters for every action except `retrieve`. Use a new key for each new operation. The same key and request replay the original success or failure without regenerating; changing the request under the same key returns 409. If submission times out, query the original task or replay with the same key before considering a new paid operation.

### Project workflow

| Action | Required inputs beyond `action` | Result and next step |
| --- | --- | --- |
| `create` | `title` (1–200 characters) | Synchronous; retain `data.id` as the project ID. |
| `retrieve` | `id` | Synchronous; read the latest `data.version_id` and complete `data.state`. |
| `save` | `id`, complete `state`, latest `version_id` | Synchronous even if a `task_id` is returned; use the new version. Only the first save of an empty project may omit `version_id`. |
| `upload` | `id`, `version_id`, public HTTPS `audio_url` | Async; read `response.data.candidate.audio_id` from the completed task. |
| `add_track` | `id`, `version_id`, completed `audio_id` | Async; add the source audio and retain the new version. |
| `render` | `id`, `version_id`, `title` | Async; read `response.data.audio_id` and `audio_url` for the mix. |
| `generate_track` | `id`, `version_id`, `source_audio_id`, `render_audio_id`, `model`, `start_seconds`, `end_seconds`, `stem_control_tags` | Async; produces candidates without changing the project. Save an empty target track before generating. |
| `replace_section` | `id`, `version_id`, `source_audio_id`, `model`, `start_seconds`, `end_seconds` | Async; produces replacement candidates without changing the project; no render reference required. |
| `commit_candidate` | `id`, `version_id`, `operation_id`, `candidate_id`, `track_id` | Async; submit a selected candidate and retain the new version. |
| `remove_track` | `id`, `version_id`, `track_id` | Synchronous; retain the new version. |

For async actions, `async=false` does not make them synchronous. Poll `POST /suno/tasks` with `{"action":"retrieve","id":"TASK_ID"}`, or set `callback_url`. A task ID means accepted, not successful: wait for `finished_at` and check `response.success`; failures are in `response.error`. See the [task result guide](docs/suno_tasks_api_integration_guide.md#project-task-results).

`save` replaces the entire state, not a partial patch. Retrieve it first, edit only the intended fields, and preserve unknown fields. Save a uniquely identified audio track with `type:"audio"` and `clips:[]` before generating a new-track candidate, because candidates are tied to that saved version. Do not create the target track after generation. Read `operation_id` and `candidates[].id` from the completed generation task, and `track_id` from the project's `state.tracks[].id`; none of these is the project ID or the new submission's task ID.

### Timing and optional controls

- `start_seconds` / `end_seconds` select a range in the source audio, with `0 ≤ start_seconds < end_seconds`. Replacement must not extend past the source duration. The selected range does not guarantee candidate output length.
- `start_beats` / `end_beats` are project timeline beats. `state.timing.bps` is positive beats per second, default 2. Clip fields `startBeats`, `endBeats`, and `readStartBeats` also use project beats. Adding 41 seconds at beat 0 gives a default end of beat 82 at 2 bps.
- `add_track` accepts `name`, `color` (default `#7251F7`), `title`, `start_beats` (default 0), `end_beats`, and nonnegative `gain` (default 1). The default end is start plus audio duration times bps.
- Generation and replacement accept `title`, `tags`, and `negative_tags`. `generate_track` always submits two candidates; do not send `batch_size`. It additionally accepts `prompt`, `instrumental` (default `true`), and `vocal_gender` (`f`, `m`, or `unspecified`, default `unspecified`). `stem_control_tags` is a description such as `add Piano`, not an enum.
- For replacement, `prompt` supplies source lyrics or context, while `replacement_lyrics` supplies the new lyrics. `fixed` defaults to `false`; `fixed=true` requires a range shorter than 26 seconds and remains unverified in the recorded workflow.
- For new-track commits, optional `name`, nonnegative `gain` (default 1), and non-overlapping `start_beats` / `end_beats` control placement. Defaults use the source clip's start and the candidate's actual duration. Replacement commits target the original track containing the unique source clip and must omit `start_beats` and `end_beats`.
- Rendering accepts `lyrics` (default `[Instrumental]`), `tags`, and an optional beat range. Without a range it uses the earliest and latest audible clips; muted clips are excluded and solo tracks take precedence. An empty or inaudible project cannot be rendered.

The generation model enums are `chirp-v3-5`, `chirp-v4`, `chirp-v4-5`, `chirp-v4-5-plus`, `chirp-v5`, `chirp-v5-5`, `chirp-v6`, `chirp-v6-wild`, and `chirp-v6-mini`. Passing validation does not guarantee that the model supports the selected operation; check the terminal task result. There is no automatic model substitution.

### Beta limitations and recovery

The recorded October 9, 2026 workflow generated and committed a new-track candidate, but rendering the project containing it failed with `studio_audio_unavailable`. Removing that candidate track and rendering the latest version succeeded. The same workflow produced 36-second replacement candidates for an 8-second selection in a 41-second source; committing one failed with `bad_request`, leaving the original track unchanged. Candidate generation, a playable URL, or a successful commit is not proof that the whole project can be rendered.

On `project_version_conflict` or `project_candidate_stale` (409), retrieve the latest project and replan; do not replay stale candidates. If a candidate duration cannot safely match the source or selected section, retain the original track and inspect the candidate rather than forcing guessed beat positions. For audio-access failures, preserve the project and check the source and `trace_id`. Do not automatically repeat paid generation to resolve these failures. Projects and candidates are bound to their application and execution environment; do not assume cross-application reuse or automatic failover. Use only audio you have rights to process and retain final exported audio URLs.

## Troubleshooting

- For authentication errors, open [Manage Keys](https://platform.acedata.cloud/console/credentials?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) to check the key’s allowed APIs, expiration and usage limit.
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
