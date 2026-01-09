# Get Document Chunks API

Retrieves a list of chunks for a specific document within a collection.

## Endpoint

```
GET /collections/{collection_id}/documents/{document_id}/version/{version}/chunks
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | Unique identifier for the collection |
| `document_id` | string | Yes | Unique identifier for the document |
| `version` | integer | Yes | Version number of the chunks to retrieve |

## Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |
| `search` | string | - | Optional search query to filter chunks by content |

## Response Schema

The response follows a standardized format with `data` containing the list of chunks and `metadata` for pagination details.

```typescript
{
  data: Array<{
    id: string
    content: string
    meta: object
    status: string
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

The `data` array contains chunk objects.

#### Chunk Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the chunk |
| `content` | string | The text content of the chunk |
| `meta` | object | Metadata associated with the chunk (e.g., page number, bbox) |
| `status` | string | Processing status of the chunk |

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
curl -X GET "http://localhost:8005/collections/123/documents/456/version/1/chunks?page=1&limit=10"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "chunk_1",
      "content": "This is the content of the first chunk...",
      "meta": {
        "page_number": 1
      },
      "status": "complete"
    },
    {
      "id": "chunk_2",
      "content": "This is the content of the second chunk...",
      "meta": {
        "page_number": 1
      },
      "status": "complete"
    }
  ],
  "metadata": {
    "page": 1,
    "limit": 10,
    "total": 20,
    "totalPages": 2,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Chunks retrieved successfully |
| `404 Not Found` | Collection or Document not found |
| `500 Internal Server Error` | Server error occurred while processing the request |
