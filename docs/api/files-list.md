# List Files API

Retrieves a paginated list of files for a specific collection with optional filtering and sorting capabilities.

## Endpoint

```
GET /api/collections/{id}/files
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the collection |

## Request Parameters

All parameters are optional query parameters.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | `1` | Page number for pagination |
| `limit` | number | `10` | Number of items per page |
| `search` | string | - | Search query to filter files by name |
| `sortBy` | string | - | Field to sort by. Options: `name`, `size`, `uploadedAt` |
| `sortOrder` | `'asc'` \| `'desc'` | - | Sort order (ascending or descending) |
| `select` | boolean | `false` | When `true`, returns only `id` and `name` fields in the data array |

## Request Schema

No request body is required for this endpoint. All parameters are passed as query strings.

## Response Schema

The response follows a standardized format with `data`, `metadata`, and `message` keys.

### Default Response (when `select=false` or not provided)

```typescript
{
  data: Array<{
    id: string
    name: string
    type: string
    size: number
    uploadedAt: string
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

### Simplified Response (when `select=true`)

```typescript
{
  data: Array<{
    id: string
    name: string
  }>
  message: string
}
```

### Data Array Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the file |
| `name` | string | Name of the file |
| `type` | string | MIME type of the file |
| `size` | number | Size of the file in bytes |
| `uploadedAt` | string | ISO 8601 date string when the file was uploaded |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `page` | number | Current page number |
| `limit` | number | Number of items per page |
| `total` | number | Total number of files matching the query |
| `totalPages` | number | Total number of pages available |
| `hasNextPage` | boolean | Whether there is a next page available |
| `hasPreviousPage` | boolean | Whether there is a previous page available |

## Example Request

```bash
curl -X GET "http://localhost:3000/api/collections/1/files?page=1&limit=10&search=document&sortBy=name&sortOrder=asc"

# Request with simplified output (only id and name)
curl -X GET "http://localhost:3000/api/collections/1/files?select=true"
```

## Example Success Response

```json
{
  "data": [
    {
      "id": "file_001",
      "name": "document1.pdf",
      "type": "application/pdf",
      "size": 1048576,
      "uploadedAt": "2024-01-15"
    },
    {
      "id": "file_002",
      "name": "document2.docx",
      "type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "size": 524288,
      "uploadedAt": "2024-01-16"
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
  "message": "Files retrieved successfully"
}
```

### Example Success Response with `select=true`

```json
{
  "data": [
    {
      "id": "file_001",
      "name": "document1.pdf"
    },
    {
      "id": "file_002",
      "name": "document2.docx"
    }
  ],
  "message": "Files retrieved successfully"
}
```

## Example Error Responses

### 400 Bad Request

```json
{
  "data": null,
  "metadata": null,
  "message": "Invalid query parameters: 'sortBy' must be one of: name, size, uploadedAt"
}
```

### 404 Not Found

```json
{
  "data": null,
  "metadata": null,
  "message": "Collection with id '1' not found"
}
```

### 500 Internal Server Error

```json
{
  "data": null,
  "metadata": null,
  "message": "Internal server error occurred while retrieving files"
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Files retrieved successfully |
| `400 Bad Request` | Invalid query parameters provided |
| `404 Not Found` | Collection not found |
| `500 Internal Server Error` | Server error occurred while processing the request |
