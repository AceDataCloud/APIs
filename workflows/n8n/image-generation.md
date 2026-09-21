# Prompt to image

[`image-generation.json`](image-generation.json) sends one prompt to `POST https://api.acedata.cloud/flux/images` and returns a structured image result. It uses only built-in n8n nodes and fails explicitly when the API returns a non-200 response or a 200 response without a usable `image_url`.

Last contract verification: **2026-09-10**.

## Import and setup

1. Download `image-generation.json`.
2. In n8n, choose **Import from File**. For CLI validation, run `n8n import:workflow --input=image-generation.json` against an isolated n8n user folder/database first.
3. The stable template ID is `acedata-image-generation-v1`. An n8n CLI import can overwrite an existing workflow with the same ID; change or remove the ID before importing if you need a separate copy.
4. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-image-generation).
5. Create a **Header Auth** credential:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
6. Select that credential in **Generate image with Ace Data Cloud**.
7. Edit `prompt`, `model`, or `size` in **Set image input**, then run the workflow.

The exported workflow contains no credential ID, token, pinned response, or user data. n8n stores credential data separately from the workflow JSON.

## Inputs

| Field | Default | Contract |
| --- | --- | --- |
| `prompt` | Editorial research-station illustration | Required generation prompt |
| `model` | `flux-2-klein` | Must remain in the endpoint model enum |
| `size` | `1024x1024` | Required image dimensions |

The request fixes `action` to `generate`, `count` to `1`, and `async` to `false`. Keeping `count=1` bounds each execution to one generated image and one unit of the model's per-image charge.

## Output and failure behavior

A successful run returns:

```json
{
  "status": "success",
  "model": "flux-2-klein",
  "prompt": "...",
  "size": "1024x1024",
  "image_url": "https://...",
  "seed": "..."
}
```

The HTTP node requests a full JSON response and treats non-2xx responses as data. Only HTTP 200 continues. A second guard requires `success: true` and a non-empty `data[0].image_url`; all other outcomes stop with the response body. The request timeout is 180 seconds.

## Cost and data boundary

- Each execution makes **one billable image-generation API call**. Billing scales with `count`; this template fixes it at one. Failed or manually retried executions can add calls. Check current pricing before activation.
- The prompt, model, size, and generation options are sent to Ace Data Cloud. The returned CDN URL is present in n8n execution data.
- Do not send secrets, personal data, or content you are not authorized to process.
- Review generated images for accuracy, rights, and policy compliance before publication.
