# Get Additional Chunks API

Retrieves a paginated list of "additional" chunks (chunks not associated with any specific document) within a collection.

## Endpoint

```
GET /collections/{collection_id}/additional-chunks
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | Unique identifier for the collection |

## Request Parameters

All parameters are optional query parameters.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |

## Response Schema

The response follows a standardized format with `data` containing the list of chunks, and `metadata` for pagination details.

```typescript
{
  data: Array<{
    id: string
    content: string
    meta: object
    status: string
    version: number
    createdAt: string
  }>
  metadata: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNextPage: boolean
    hasPreviousPage: boolean
  }
}
```

### Data Fields

The `data` field is an array of chunk objects where `document_id` is null.

#### Chunk Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the chunk |
| `content` | string | The text content of the chunk |
| `meta` | object | Metadata associated with the chunk |
| `status` | string | Processing status of the chunk |
| `version` | number | Version of the chunk |
| `createdAt` | string | ISO 8601 date string when the chunk was created |

### Meta Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | Current page number |
| `limit` | number | Number of items per page |
| `total` | number | Total number of chunks matching the query |
| `totalPages` | number | Total number of pages available |
| `hasNextPage` | boolean | Whether there is a next page available |
| `hasPreviousPage` | boolean | Whether there is a previous page available |

## Example Request

```bash
curl -X GET "http://localhost:8005/collections/123/additional-chunks?page=1&limit=10"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "chunk_1",
      "content": "This is an additional chunk content...",
      "meta": {
        "source": "manual_entry"
      },
      "status": "completed",
      "version": 1,
      "createdAt": "2024-01-15T10:00:00Z"
    },
    {
      "id": "chunk_2",
      "content": "Another additional chunk...",
      "meta": {
         "source": "api_upload"
      },
      "status": "pending",
      "version": 1,
      "createdAt": "2024-01-15T10:05:00Z"
    }
  ],
  "metadata": {
    "page": 1,
    "limit": 10,
    "total": 2,
    "totalPages": 1,
    "hasNextPage": false,
    "hasPreviousPage": false
  }
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Chunks retrieved successfully |
| `400 Bad Request` | Invalid parameters provided |
| `404 Not Found` | Collection not found |
| `500 Internal Server Error` | Server error occurred |
