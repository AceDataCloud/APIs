# Fish Model Query API Integration Guide

`GET https://api.acedata.cloud/fish/model`

List public voices or voices created by the authenticated account.

## Query Parameters

`page_size` (default `10`), `page_number` (default `1`), `title`, `tag`, `self`, `author_id`, `language`, `title_language`, and `sort_by` are supported. Set `self=true` to list your own voices.

```bash
curl --get 'https://api.acedata.cloud/fish/model' \
  --header 'Authorization: ******' \
  --data-urlencode 'language=en' \
  --data-urlencode 'tag=narration' \
  --data-urlencode 'page_size=10'
```

The response is `{"total": 1, "items": [<model entities>]}`. Each entity's `_id` can be used as the Fish TTS `reference_id`.
