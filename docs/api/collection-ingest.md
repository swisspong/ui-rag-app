# Ingest Collection API

Ingests a document into a collection.

## Endpoint

```
POST /collections/ingest
```

## Request Headers

| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |
| accept | application/json | Yes |

## Request Body

The request body must be a JSON object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| document_id | string | Yes | Unique identifier for the document |
| collection_id | string | Yes | Unique identifier for the collection |
| version | integer | Yes | Version of the document |
| status | string | Yes | Status of the ingestion defined as 'pending' or 'failed' |

### Request Schema

```typescript
{
  document_id: string;   // Required: Unique document ID
  collection_id: string; // Required: Unique collection ID
  version: number;       // Required: Document version
  status: 'pending' | 'failed'; // Required: Ingestion status
}
```

## Response Body

The response indicates the result of the ingestion request.

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Indicates if the request was successful |

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
  'http://localhost:8005/collections/ingest' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_id": "string",
  "collection_id": "string",
  "version": 0,
  "status": "pending"
}'
```

### JSON Payload

```json
{
  "document_id": "string",
  "collection_id": "string",
  "version": 0,
  "status": "pending"
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
| 200 | OK - Ingestion request processed successfully |
| 422 | Validation Error - Invalid request data |
| 500 | Internal Server Error - Server encountered an unexpected error |
