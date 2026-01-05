# List Collections API

Retrieves a paginated list of collections with optional filtering and sorting capabilities.

## Endpoint

```
GET /api/collections
```

## Request Parameters

All parameters are optional query parameters.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |
| `search` | string | - | Search query to filter collections by name or description |
| `sortBy` | string | - | Field to sort by. Options: `name`, `createdAt`, `fileCount` |
| `sortOrder` | `'asc'` \| `'desc'` | - | Sort order (ascending or descending) |

## Request Schema

No request body is required for this endpoint. All parameters are passed as query strings.

## Response Schema

The response follows a standardized format with `data`, `metadata`, and `message` keys.

```typescript
{
  data: Array<{
    id: string
    name: string
    description: string
    fileCount: number
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
  message: string
}
```

### Data Array Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the collection |
| `name` | string | Name of the collection |
| `description` | string | Description of the collection |
| `fileCount` | number | Number of files in the collection |
| `createdAt` | string | ISO 8601 date string when the collection was created |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | Current page number |
| `limit` | number | Number of items per page |
| `total` | number | Total number of collections matching the query |
| `totalPages` | number | Total number of pages available |
| `hasNextPage` | boolean | Whether there is a next page available |
| `hasPreviousPage` | boolean | Whether there is a previous page available |

## Example Request

```bash
curl -X GET "http://localhost:8005/collections?page=1&limit=10&search=product&sortBy=name&sortOrder=asc"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "1",
      "name": "Product Documentation",
      "description": "All product manuals and user guides",
      "fileCount": 15,
      "createdAt": "2024-01-15"
    },
    {
      "id": "2",
      "name": "Product FAQs",
      "description": "Frequently asked questions about products",
      "fileCount": 8,
      "createdAt": "2024-01-20"
    }
  ],
  "metadata": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "totalPages": 3,
    "hasNextPage": true,
    "hasPreviousPage": false
  },
  "message": "Collections retrieved successfully"
}
```

## Example Error Responses

### 400 Bad Request

```json
{
  "data": null,
  "metadata": null,
  "message": "Invalid query parameters: 'sortBy' must be one of: name, createdAt, fileCount"
}
```

### 500 Internal Server Error

```json
{
  "data": null,
  "metadata": null,
  "message": "Internal server error occurred while retrieving collections"
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Collections retrieved successfully |
| `400 Bad Request` | Invalid query parameters provided |
| `500 Internal Server Error` | Server error occurred while processing the request |
