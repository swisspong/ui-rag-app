# List Documents in Collection API

Retrieves a paginated list of documents within a specific collection.

## Endpoint

```
GET /collection/{collectionId}/documents
```

## Request Parameters

All parameters are optional query parameters.


| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |
| `search` | string | - | Optional search query to filter documents by content or filename |
| `select` | boolean | `false` | If `true`, returns all documents (ignoring pagination) with a simplified structure (`id`, `name`, `metadata`: `null`) |

## Request Schema

No request body is required for this endpoint. All parameters are passed as query strings.

## Response Schema

The response follows a standardized format with `data` containing the list of documents, and `meta` for pagination details.

```typescript
{
  data: Array<{
    id: string
    name: string
    filename: string
    content: string
    status: string
    createdAt: string
  }>
  meta: {
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

The `data` field is an array of document objects.

#### Document Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the document |
| `name` | string | Name of the document |
| `filename` | string | Original filename |
| `content` | string | text content of the document |
| `status` | string | Status of the document (e.g. pending, completed) |
| `createdAt` | string | ISO 8601 date string when the document was created |

### Meta Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | Current page number |
| `limit` | number | Number of items per page |
| `total` | number | Total number of documents matching the query |
| `totalPages` | number | Total number of pages available |
| `hasNextPage` | boolean | Whether there is a next page available |
| `hasPreviousPage` | boolean | Whether there is a previous page available |

### Selection Mode Response (select=true)

When `select=true` is provided, the API returns a list of all documents without pagination. The document objects are simplified to include only `id`, `name`, and `metadata` (which is `null`).

```typescript
{
  data: Array<{
    id: string
    name: string
    metadata: null
  }>
}
```

## Example Request

```bash
curl -X GET "http://localhost:8005/collection/123/documents?page=1&limit=10"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "doc_1",
      "name": "Invoice 123",
      "filename": "invoice.pdf",
      "content": "Invoice #123...",
      "status": "completed",
      "createdAt": "2024-01-15T10:00:00Z"
    },
    {
      "id": "doc_2",
      "name": "Meeting Notes",
      "filename": "notes.txt",
      "content": "Meeting notes...",
      "status": "pending",
      "createdAt": "2024-01-15T11:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 20,
    "totalPages": 2,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

## Example Selection Mode Request

```bash
curl -X GET "http://localhost:8005/collection/123/documents?select=true"
```

## Example Selection Mode Response

```json
{
  "data": [
    {
      "id": "doc_1",
      "name": "Invoice 123",
      "metadata": null
    },
    {
      "id": "doc_2",
      "name": "Meeting Notes",
      "metadata": null
    }
  ]
}
```


## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Documents retrieved successfully |
| `400 Bad Request` | Invalid query parameters provided |
| `404 Not Found` | Collection not found |
| `500 Internal Server Error` | Server error occurred while processing the request |
