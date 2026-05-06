---
title: "Suno MIDI Generation API 对接说明"
description: "Suno Music Generation 集成指南 - Ace Data Cloud"
---

SUNO 允许我们对生成的音乐进行二次创作，获取音乐的MIDI，本文档讲解相关 API 的对接方法。

该 API 核心输入参数是 `audio_id`，它是官方生成的歌曲ID，一般是全音轨分离的歌曲ID（对应[歌曲生成](https://platform.acedata.cloud/documents/suno-audios)中参数`action`为`all_stems`）。可选还支持 `callback_url` 异步回调地址。

这里我们输入的 `audio_id` 是 `c65e6ffd-ead3-4926-9c8c-a42ce202946b`。

```python
import requests

url = "https://api.acedata.cloud/suno/midi"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "audio_id": "c65e6ffd-ead3-4926-9c8c-a42ce202946b"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

结果如下：

```json
{
  "success": true,
  "task_id": "4f94486d-5013-4bcc-922f-39bd52b5cd4a",
  "trace_id": "8bc8cca3-2d4b-46d0-a4fa-bb355af9902c",
  "data": [
    {
      "state": "complete",
      "instruments": [
        {
          "name": "Synth Voice",
          "notes": [
            {
              "pitch": 55,
              "start": 29.78125,
              "end": 31.78125,
              "velocity": 0.49606299212598426
            },
            {
              "pitch": 52,
              "start": 32.807291666666664,
              "end": 32.9375,
              "velocity": 0.49606299212598426
            }
          ]
        }
      ]
    }
  ]
}
```

可以看到，`data` 里面的字段就是全音轨分离后歌曲的MIDI信息。
