# Ace Data Cloud n8n workflows

## SERP research

[`serp-research.json`](serp-research.json) is a three-node workflow:

1. start with a Manual Trigger;
2. edit the query, result type, and result count;
3. call `POST https://api.acedata.cloud/serp/google` through n8n's HTTP Request node.

### Import

1. Download `serp-research.json`.
2. In n8n, choose **Import from File** and select it. The template ID is `acedata-serp-research-v1`; change it in the JSON first if you want a separate copy instead of updating an earlier CLI import.
3. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-serp-research).
4. Create an **Header Auth** credential in n8n:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
5. Open **Search with Ace Data Cloud** and select that Header Auth credential.
6. Edit the values in **Set search input**, then run the workflow.

The exported workflow contains no credential ID or secret. n8n stores the Header Auth credential separately and does not include credential data in workflow exports.

### Inputs

| Field | Default | Meaning |
|---|---|---|
| `query` | `Ace Data Cloud MCP` | Search query |
| `type` | `search` | `search`, `images`, `news`, `maps`, `places`, or `videos` |
| `number` | `10` | Results per page |

The HTTP node returns the structured API response to the workflow. Errors include a code/message and may include a `trace_id` for support.

### Security

- Keep tokens in n8n credentials, never in Set/Edit Fields or the workflow JSON.
- Do not publish an exported workflow until you have checked it for pinned data and secrets.
- Search queries can contain sensitive information; send only data you are authorized to process.
