# Document Chunking API

Triggers the chunking process for specific documents within a collection.

## Endpoint

```
POST /collections/{collection_id}/chunking
```

## Request Headers

| Header       | Value            | Required |
| ------------ | ---------------- | -------- |
| Content-Type | application/json | Yes      |

## Path Parameters

| Parameter     | Type   | Required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| collection_id | string | Yes      | The unique ID of the collection |

## Request Body

The request body must be a JSON object with the following fields:

| Field        | Type            | Required | Description                                      |
| ------------ | --------------- | -------- | ------------------------------------------------ |
| document_ids | array of strings| Yes      | List of document IDs to be chunked               |

### Request Schema

```typescript
{
  document_ids: string[]; // Required: List of document IDs
}
```

## Response Body

The response returns a success status.

### Response Schema

```typescript
{
  success: boolean;
}
```

## Example Request

### cURL

```bash
curl -X POST http://localhost:8005/collections/123e4567-e89b-12d3-a456-426614174000/chunking \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": [
      "doc_1",
      "doc_2"
    ]
  }'
```

### JSON Payload

```json
{
  "document_ids": [
    "doc_1",
    "doc_2"
  ]
}
```

## Example Success Response

**Status Code:** 200 OK

```json
{
  "success": true
}
```

## Status Codes

| Status Code | Description                                      |
| ----------- | ------------------------------------------------ |
| 200         | OK - Chunking process initiated successfully     |
| 400         | Bad Request - Invalid request data               |
| 404         | Not Found - Collection or Documents not found    |
| 500         | Internal Server Error - Unexpected server error  |
