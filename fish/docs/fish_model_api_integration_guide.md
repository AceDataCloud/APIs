# Fish Model Create API Integration Guide

`POST https://api.acedata.cloud/fish/model`

Create a cloned voice from a publicly accessible audio sample. Send your API token in the `Authorization` header and `application/json` content.

## Request Body

| Field | Type | Required | Description |
|---|---|---:|---|
| `title` | string | yes | Voice name |
| `voices` | string | yes | One public HTTP(S) audio URL; not an array |
| `description` | string | no | Voice description |
| `cover_image` | string | no | Public cover-image URL |
| `visibility` | string | no | `private` (default) or `public` |
| `tags` / `texts` | string[] | no | Search tags / texts for reference samples |
| `enhance_audio_quality` / `generate_sample` | boolean | no | Enhance samples / generate a sample after training |

```bash
curl --request POST 'https://api.acedata.cloud/fish/model' \
  --header 'Authorization: ******' \
  --header 'Content-Type: application/json' \
  --data '{"title":"My voice","voices":"https://example.com/sample.mp3","visibility":"private"}'
```

The response is a model entity. Use its `_id` as `reference_id` in `POST /fish/tts`.
