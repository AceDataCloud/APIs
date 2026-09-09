# OpenAI Realtime API (`/v1/realtime`)

The Realtime API provides low-latency speech-to-speech communication over a WebSocket using the OpenAI Realtime GA event protocol.

## Connect

Connect to:

```text
wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1&voice=alloy
```

Server-side clients authenticate with an `Authorization: ******` header. Browser clients pass two WebSocket subprotocols: `realtime` and `acedata-token.<token>`. Do not expose a long-lived application token in untrusted client code.

Supported models are:

- `gpt-realtime-2.1` (default)
- `gpt-realtime-2.1-mini`
- `gpt-realtime-2`
- `gpt-realtime`
- `gpt-realtime-mini`

Supported voices are `alloy` (default), `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`.

## Events

After connecting, exchange OpenAI Realtime JSON events such as:

```json
{
  "type": "session.update",
  "session": {
    "instructions": "Respond briefly and clearly.",
    "audio": {
      "input": {
        "turn_detection": {
          "type": "server_vad"
        }
      }
    }
  }
}
```

Send PCM16 24 kHz mono chunks with `input_audio_buffer.append`, then request output with `response.create`. Audio arrives in `response.output_audio.delta` events, and `response.done` contains final status and usage.

The relay fixes transport, output voice, transcription, and noise-reduction settings when the connection is established. A `session.update` can change supported GA fields such as `instructions`, `tools`, `tool_choice`, `output_modalities`, `reasoning`, `parallel_tool_calls`, and turn detection. Attempts to change fixed fields, exceed the output-token cap, or use unsupported fields produce a recoverable `error` event while the WebSocket remains open.

The handshake returns `401` for invalid authentication and `403` for insufficient balance. Billing is calculated per assistant turn from `response.done.usage`.
