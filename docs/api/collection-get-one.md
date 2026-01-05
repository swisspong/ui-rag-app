# Get Collection API

Retrieves a single collection by its unique identifier. This endpoint returns detailed information about a specific collection including its name, description, file count, and creation date.

## Endpoint

```
GET /api/collections/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier for the collection |

## Request Body

No request body is required for this endpoint.

## Response Body

The response body contains the collection details in a `data` field, along with a `message` field:

| Field | Type | Description |
|-------|------|-------------|
| data | object | Object containing the collection details |
| data.id | string | Unique identifier for the collection |
| data.name | string | Collection name |
| data.description | string | Collection description |
| data.fileCount | number | Number of files in the collection |
| data.createdAt | string | ISO date format (YYYY-MM-DD) |
| message | string | Success message describing the operation result |

### Response Schema

```typescript
{
  data: {
    id: string;           // Unique identifier for the collection
    name: string;         // Collection name
    description: string;  // Collection description
    fileCount: number; // Number of files in the collection
    createdAt: string;    // ISO date format (YYYY-MM-DD)
  };
  message: string;        // Success message
}
```

## Example Request

### cURL

```bash
curl -X GET http://localhost:3000/api/collections/1
```

## Example Success Response

**Status Code:** 200 OK

```json
{
  "data": {
    "id": "1",
    "name": "Product Documentation",
    "description": "All product manuals and user guides",
    "fileCount": 15,
    "createdAt": "2024-01-15"
  },
  "message": "Collection retrieved successfully"
}
```

## Example Error Responses

### 400 Bad Request - Invalid ID Format

**Status Code:** 400 Bad Request

```json
{
  "error": "Bad Request",
  "message": "Invalid collection ID format"
}
```

### 404 Not Found - Collection Not Found

**Status Code:** 404 Not Found

```json
{
  "error": "Not Found",
  "message": "Collection with ID '999' not found"
}
```

### 500 Internal Server Error

**Status Code:** 500 Internal Server Error

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred while retrieving the collection"
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Collection retrieved successfully |
| 400 | Bad Request - Invalid ID format or malformed request |
| 404 | Not Found - Collection with the specified ID does not exist |
| 500 | Internal Server Error - Server encountered an unexpected error |
