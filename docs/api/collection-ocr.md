# Process OCR API

Initiates OCR processing for specific files within a collection.

## Endpoint

```
POST /api/collections/{collection_id}/ocr
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | Unique identifier for the collection |

## Request Headers

| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |
| accept | application/json | Yes |

## Request Body

The request body must be a JSON object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `collection_file_ids` | array<string> | Yes | List of file IDs within the collection to process |

### Request Schema

```typescript
{
  collection_file_ids: string[]; // Required: List of file IDs
}
```

## Response Body

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Indicates if the OCR processing was initiated successfully |

### Response Schema

```typescript
{
  success: boolean;
}
```

## Example Request

### cURL

```bash
curl -X 'POST' \
  'http://localhost:8005/api/collections/id1/ocr' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "collection_file_ids": [
    "file_id_1"
  ]
}'
```

### JSON Payload

```json
{
  "collection_file_ids": [
    "file_id_1"
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

| Status Code | Description |
|-------------|-------------|
| `200 OK` | OCR processing initiated successfully |
| `422 Validation Error` | Invalid request data |
| `500 Internal Server Error` | Server error processing request |
