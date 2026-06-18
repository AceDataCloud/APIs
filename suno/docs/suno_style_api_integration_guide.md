# Suno Style API Integration Instructions

SUNO allows us to input prompts to generate enhanced song styles. This document explains the integration method for the related API.

The API has only one input parameter, which is `prompt`, the style prompt that needs to be optimized.

Here, the `prompt` we input is `A song for Christmas`.

```python
import requests

url = "https://api.acedata.cloud/suno/style"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "prompt": "A song for Christmas"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The result is as follows:

```json
{
  "success": true,
  "task_id": "8e887548-7185-48a9-b7cb-e51754f7b87b",
  "trace_id": "ac4ec363-4245-400b-9643-0b6fed8c6b20",
  "data": [
    {
      "file_url": "https://cdn1.suno.ai/style_8e887548-7185-48a9-b7cb-e51754f7b87b.json"
    }
  ]
}
```

As can be seen, the `file_url` field in `data` is the URL to the generated style result.