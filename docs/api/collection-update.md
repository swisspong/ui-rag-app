# Update Collection API

Updates an existing collection in the system. This endpoint allows you to modify the name and/or description of a collection identified by its unique ID.

## Endpoint

```
PATCH /api/collections/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier for the collection to update |

## Request Headers

| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |

## Request Body

The request body must be a JSON object with the following fields:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| name | string | Yes | 2-100 characters | The updated name of the collection |
| description | string | No | Max 500 characters | Updated description of the collection |

### Request Schema

```typescript
{
  name: string;        // Required: 2-100 characters
  description?: string; // Optional: max 500 characters
}
```

## Response Body

The response body contains the updated collection details in a `data` field, along with a `message` field:

| Field | Type | Description |
|-------|------|-------------|
| data | object | Object containing the updated collection details |
| data.id | string | Unique identifier for the collection |
| data.name | string | Updated collection name |
| data.description | string | Updated collection description |
| data.documentCount | number | Number of documents in the collection |
| data.createdAt | string | ISO date format (YYYY-MM-DD) |
| message | string | Success message describing the operation result |

### Response Schema

```typescript
{
  data: {
    id: string;           // Unique identifier for the collection
    name: string;         // Updated collection name
    description: string;  // Updated collection description
    documentCount: number; // Number of documents in the collection
    createdAt: string;    // ISO date format (YYYY-MM-DD)
  };
  message: string;        // Success message
}
```

## Example Request

### cURL

```bash
curl -X PATCH http://localhost:3000/api/collections/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Documentation",
    "description": "Updated description"
  }'
```

### JSON Payload

```json
{
  "name": "Updated Product Documentation",
  "description": "Updated description"
}
```

## Example Success Response

**Status Code:** 200 OK

```json
{
  "data": {
    "id": "1",
    "name": "Updated Product Documentation",
    "description": "Updated description",
    "documentCount": 15,
    "createdAt": "2024-01-15"
  },
  "message": "Collection updated successfully"
}
```

## Example Error Responses

### 400 Bad Request - Validation Error

**Status Code:** 400 Bad Request

```json
{
  "error": "Validation Error",
  "message": "Name must be between 2 and 100 characters"
}
```

Or:

```json
{
  "error": "Validation Error",
  "message": "Description must not exceed 500 characters"
}
```

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
  "message": "An unexpected error occurred while updating the collection"
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Collection updated successfully |
| 400 | Bad Request - Invalid request data, validation errors, or invalid ID format |
| 404 | Not Found - Collection with the specified ID does not exist |
| 500 | Internal Server Error - Server encountered an unexpected error |
