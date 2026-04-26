# OpenAI Chat Completion 4o Image API Application and Usage

OpenAI ChatGPT is a very powerful AI dialogue system that can generate fluent and natural replies in just a few seconds after inputting a prompt. ChatGPT stands out in the industry for its excellent language understanding and generation capabilities. Today, ChatGPT is widely used in various industries and fields, with increasing influence. Whether it is daily conversation, creative writing, professional consulting, or code programming, ChatGPT can provide amazing intelligent assistance, greatly improving human work efficiency and creativity.

This document mainly describes the usage process of the OpenAI Chat Completion 4o Image API, which allows us to easily use the official OpenAI ChatGPT multimodal conversation features.

## Application Process

To use the OpenAI Chat Completion 4o Image API, you can first visit the [OpenAI Chat Completion 4o Image API](https://platform.acedata.cloud/documents/1bcf3bba-102b-495d-9bba-47cd96717e45) page and click the "Acquire" button to obtain the credentials needed for the request:

![](https://cdn.acedata.cloud/nyq0xz.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

Upon the first application, there will be a free quota provided, allowing you to use the API for free.

## GPT-4o Image Model

### Generate Image from Reference Image

Below is an example of generating an image in a custom style based on a reference image. First, let's look at the input image:

![](https://cdn.acedata.cloud/qzx2z1.png)

You can see that the reference image is a real person's photo. We can transform it into a different style, such as anime style. Here is a specific request example:

```json
{
  "model": "gpt-4o-image",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate an anime-style image with a hat"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://cdn.acedata.cloud/qzx2z1.png"
          }
        }
      ]
    }
  ],
  "stream": false
}
```

Sample result:

```json
{
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "> ❇️ 关键字：https://file.onechats.ai/tem/f7b8024b6f430a0a9d20174bcec1ad3a.png 生成动漫风格的图片，并且带上个帽子\n\n> ✨ Sora正在绘制图片中...\n\n> 🏃 进度：8.4%\n\n> 🏃 进度：17.5%\n\n> 🏃 进度：25.9%\n\n> 🏃 进度：34.3%\n\n> 🏃 进度：43.4%\n\n> 🏃 进度：51.8%\n\n> 🏃 进度：60.9%\n\n> 🏃 进度：71.4%\n\n> 🏃 进度：76.3%\n\n> 🏃 进度：80.4%\n\n> 🏃 进度：83.8%\n\n> 🏃 进度：86.6%\n\n> 🏃 进度：88.9%\n\n> 🏃 进度：90.8%\n\n> 🏃 进度：92.4%\n\n> ✅ 图片绘制成功，请注意查收~~~\n\n![](https://file.onechats.ai/tem/4abe605b362a9a59028bf7fafa5f2aff.png)\n\n"
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1745152859,
  "id": "chatcmpl-7c43d1dd-17e3-4513-9aec-899b21be3c2a",
  "model": "gpt-4o-image",
  "object": "chat.completion.chunk",
  "usage": {
    "prompt_tokens": 68,
    "completion_tokens": 19,
    "total_tokens": 87
  }
}
```

The `message` inside `choices` contains the complete conversation result, and the image result is also included in the conversation result. You can see that the generated image is in anime style, as shown below:

<p><img src="https://cdn.acedata.cloud/qmr391.jpg" width="400" class="m-auto"></p>

### Text-to-Image Generation

You can generate an image from a text prompt, and the result will be returned in a conversational format. Below is an example using the prompt "Create a picture of a futuristic city at sunset":

```json
{
  "model": "gpt-4o-image",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Create a picture of a futuristic city at sunset"
        }
      ]
    }
  ],
  "stream": false
}
```

Sample result:

```json
{
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "> ❇️ 关键字：创建一张未来城市日落的图片\n\n> ✨ Sora正在绘制图片中...\n\n> 🏃 进度：9.8%\n\n> 🏃 进度：19.6%\n\n> 🏃 进度：30.1%\n\n> 🏃 进度：39.9%\n\n> 🏃 进度：50.4%\n\n> 🏃 进度：60.2%\n\n> 🏃 进度：69.3%\n\n> ✅ 图片绘制成功，请注意查收~~~\n\n![](https://file.onechats.ai/tem/4ab6f3cd886aaa6fd575dd37327fae59.png)\n\n"
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1745153373,
  "id": "chatcmpl-29ed630a-c8fc-4a8a-a8e0-737fcc515192",
  "model": "gpt-4o-image",
  "object": "chat.completion.chunk",
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 11,
    "total_tokens": 43
  }
}
```

The result matches the prompt, as shown below:

<p><img src="https://cdn.acedata.cloud/q502uk.jpg" width="400" class="m-auto"></p>

### Multi-image to Single Image

You can use multiple reference images to generate a single image. For example, using a handsome man photo and a coffee photo, you can generate an image of the man holding coffee. Here are the reference images:

<p><img src="https://cdn.acedata.cloud/pqquv3.jpg" width="400" class="m-auto"></p>

<p><img src="https://cdn.acedata.cloud/h8j2i0.jpg" width="400" class="m-auto"></p>

Below is a specific example using the prompt "Generate a man holding coffee and about to drink it":

```json
{
  "model": "gpt-4o-image",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Generate a man holding coffee and about to drink it"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://cdn.acedata.cloud/pqquv3.jpg"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://cdn.acedata.cloud/h8j2i0.jpg"
          }
        }
      ]
    }
  ],
  "stream": false
}
```

Sample result:

```json
{
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "> ❇️ 关键字：https://file.onechats.ai/tem/b5e2049e82ef071a804d6769e580b702.png https://file.onechats.ai/tem/78e9aa8a0dbd529f3904a6629329ebbe.png 生成男生举着咖啡，并且马上要喝的样子\n\n> ✨ Sora正在绘制图片中...\n\n> 🏃 进度：11.2%\n\n> 🏃 进度：25.9%\n\n> 🏃 进度：39.9%\n\n> 🏃 进度：47.6%\n\n> 🏃 进度：55.3%\n\n> 🏃 进度：73.3%\n\n> 🏃 进度：78.0%\n\n> 🏃 进度：81.8%\n\n> ✅ 图片绘制成功，请注意查收~~~\n\n![](https://file.onechats.ai/tem/6aa9ad6c26b9d4500ea84ea9f56e331b.png)\n\n"
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1745154125,
  "id": "chatcmpl-d6e5fc71-4e33-4ad6-b259-357241d7c1ab",
  "model": "gpt-4o-image",
  "object": "chat.completion.chunk",
  "usage": {
    "prompt_tokens": 106,
    "completion_tokens": 12,
    "total_tokens": 118
  }
}
```

You can see that the generated result indeed combines the two reference images, as shown below:

<p><img src="https://cdn.acedata.cloud/89vnpx.jpg" width="400" class="m-auto"></p>

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Conclusion

Through this document, you have learned how to use the OpenAI Chat Completion 4o Image API to easily utilize the official OpenAI ChatGPT multimodal image processing features. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
