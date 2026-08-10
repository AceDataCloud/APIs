# Gemini Generate Content API Application and Usage

Google Gemini is a very powerful AI conversation system that can generate smooth and natural replies in just a few seconds by inputting prompts. This document mainly describes the usage of the Gemini Generate Content API, which is Google's official native API format, supporting both `generateContent` and `streamGenerateContent` endpoints.

## Difference from Chat Completions API

The Gemini Generate Content API uses Google's official native request format (`contents` field), rather than the OpenAI-compatible format (`messages` field). If you are already using the Google Gemini SDK or are familiar with the official API format, you can use this API directly without modifying the request format.

The current OpenAPI documents `contents` as the required request body field. It also accepts optional `systemInstruction`, `generationConfig`, `tools`, `toolConfig`, and `safetySettings` fields.

## Application Process

Create an API Token in the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications), then send it in the `Authorization` header for Gemini requests.

One API Token works across Ace Data Cloud services. New accounts receive starter credit, and you can top up shared balance in the [console](https://platform.acedata.cloud/console/coin).

Full documentation: [Gemini Generate Content API](https://platform.acedata.cloud/documents/gemini-generate-content-api)

## Basic Usage

### Non-Streaming

Send a POST request to `/v1beta/models/{model}:generateContent`:

```bash
curl -X POST "https://api.acedata.cloud/v1beta/models/gemini-2.5-flash:generateContent" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Hello, please introduce yourself"
          }
        ]
      }
    ]
  }'
```

Example return result:

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Hello! I am Gemini, a large language model developed by Google..."
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 150,
    "totalTokenCount": 160
  },
  "modelVersion": "gemini-2.5-flash"
}
```

### Streaming

Send a POST request to `/v1beta/models/{model}:streamGenerateContent?alt=sse`:

```bash
curl -X POST "https://api.acedata.cloud/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Write a short poem about spring"
          }
        ]
      }
    ]
  }'
```

Streaming responses return content incrementally in SSE (Server-Sent Events) format.

## Common Model Values

| Model Name | Description |
|---------|------|
| `gemini-3.1-pro` | Advanced reasoning and multimodal capabilities |
| `gemini-3.5-flash` | Fast general-purpose Gemini chat/generation model |
| `gemini-3.1-flash-lite-preview` | Lightweight Gemini 3.1 variant |
| `gemini-3.0-pro` | Gemini 3.0 multimodal model |
| `gemini-3-flash-preview` | Preview flash model |
| `gemini-2.5-pro` | Strong reasoning for complex tasks |
| `gemini-2.5-flash` | Good cost/performance balance |
| `gemini-2.5-flash-lite` | Lower-cost flash-lite variant |
| `gemini-2.0-flash` | Earlier Gemini 2.0 flash model |

## Advanced Features

### System Instructions

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Hello"}]
    }
  ],
  "systemInstruction": {
    "parts": [{"text": "You are a professional poet. All replies should be in poetic form."}]
  }
}
```

### Generation Configuration

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Tell me a story"}]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 1024,
    "topP": 0.9,
    "topK": 40
  }
}
```

### JSON Mode

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "List three cities and their populations"}]
    }
  ],
  "generationConfig": {
    "responseMimeType": "application/json",
    "responseSchema": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "city": {"type": "string"},
          "population": {"type": "integer"}
        }
      }
    }
  }
}
```

### Thinking Mode

Models that support thinking (such as gemini-2.5-flash, gemini-2.5-pro) can enable thinking mode:

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Explain quantum entanglement"}]
    }
  ],
  "generationConfig": {
    "thinkingConfig": {
      "includeThoughts": true,
      "thinkingBudget": 2048
    }
  }
}
```

### Function Calling

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "What is the weather like in London right now?"}]
    }
  ],
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "get_weather",
          "description": "Get weather information for a specified city",
          "parameters": {
            "type": "object",
            "properties": {
              "city": {
                "type": "string",
                "description": "City name"
              }
            },
            "required": ["city"]
          }
        }
      ]
    }
  ]
}
```

If you need additional control over how tools are selected or invoked, the request body also accepts a `toolConfig` object in the native Gemini format.

### Multi-turn Conversation

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Hello, my name is John"}]
    },
    {
      "role": "model",
      "parts": [{"text": "Hello John! Nice to meet you."}]
    },
    {
      "role": "user",
      "parts": [{"text": "What is my name?"}]
    }
  ]
}
```

### Image Understanding

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {"text": "Describe this image"},
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "base64_encoded_image_data..."
          }
        }
      ]
    }
  ]
}
```

## Safety Settings

You can control content filtering via `safetySettings`:

```json
{
  "contents": [...],
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_ONLY_HIGH"
    }
  ]
}
```

## Error Handling

The current Gemini OpenAPI explicitly documents the following error for the native `generateContent` endpoint:

| HTTP Status Code | Meaning |
|------------|------|
| 400 | Invalid request parameters |

Authentication still uses the standard `Authorization` header, and successful streaming calls return Server-Sent Events from `streamGenerateContent`.
