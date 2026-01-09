# List Documents in Collection API

Retrieves a paginated list of documents within a specific collection.

## Endpoint

```
GET /collection/{collectionId}/documentChunks
```

## Request Parameters

All parameters are optional query parameters.


| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |
| `search` | string | - | Optional search query to filter documents by content or filename |


## Request Schema

No request body is required for this endpoint. All parameters are passed as query strings.

## Response Schema

The response follows a standardized format with `data` containing the list of documents, and `meta` for pagination details.

```typescript
{
  data: Array<{
    id: string
    version: number
    name: string
    chunkCount: number
    createdAt: string
  }>
  metadata: {
    page: number
    limit: number
    total: number
    hasNextPage: boolean
    hasPreviousPage: boolean
  }
}
```

### Data Fields

The `data` field is an array of document objects.

#### Document Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the document |
| `version` | number | Current version of the document |
| `name` | string | Name of the document |
| `chunkCount` | number | Total number of chunks in the document |
| `createdAt` | string | ISO 8601 date string when the document was created |

### Meta Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | Current page number |
| `limit` | number | Number of items per page |
| `total` | number | Total number of documents matching the query |
| `hasNextPage` | boolean | Whether there is a next page available |
| `hasPreviousPage` | boolean | Whether there is a previous page available |



## Example Request

```bash
curl -X GET "http://localhost:8005/collection/123/documentChunks?page=1&limit=10"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "doc_1",
      "version": 1,
      "name": "Invoice 123",
      "chunkCount": 5,
      "createdAt": "2024-01-15T10:00:00Z"
    },
    {
      "id": "doc_2",
      "version": 2,
      "name": "Meeting Notes",
      "chunkCount": 12,
      "createdAt": "2024-01-15T11:00:00Z"
    }
  ],
  "metadata": {
    "page": 1,
    "limit": 10,
    "total": 20,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```




## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Documents retrieved successfully |
| `400 Bad Request` | Invalid query parameters provided |
| `404 Not Found` | Collection not found |
| `500 Internal Server Error` | Server error occurred while processing the request |
