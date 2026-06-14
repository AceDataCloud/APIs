# Midjourney Seed API Integration Instructions

This guide explains how to call the Midjourney Seed API to retrieve the seed value for an existing Midjourney image.

## Application Process

To use the Midjourney Seed API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and then returned automatically.

**A single API Token works across every service on the platform.** New accounts receive free starter credit, and you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Basic Usage

Send a `POST` request to `https://api.acedata.cloud/midjourney/seed` with your API token and the `image_id` returned by a Midjourney generation task.

### Request Headers

- `accept`: set to `application/json`.
- `authorization`: add your API token in this header.
- `content-type`: set to `application/json`.

### Request Body

- `image_id` (required): Midjourney Seed Image Id

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/midjourney/seed' \
-H 'accept: application/json' \
-H 'authorization: YOUR_API_TOKEN' \
-H 'content-type: application/json' \
-d '{
  "image_id": "1515630083539206144"
}'
```

### Success Response Example

```json
{
  "seed": "1515630083539206144"
}
```

The response includes:

- `seed`: Midjourney Seed Response 200 Seed

## Error Handling

If an error occurs, the API may return one of these statuses:

- `400`: bad request, usually caused by missing or invalid parameters.
- `401`: unauthorized, invalid or missing authorization token.
- `429`: too many requests, you have exceeded the rate limit.
- `500`: internal server error.

## Conclusion

Use the Midjourney Seed API whenever you need to inspect the seed associated with a generated Midjourney image.
