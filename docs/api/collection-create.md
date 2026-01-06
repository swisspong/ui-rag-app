# Create Collection API

Creates a new collection in the system. Collections are used to organize and group related documents together.

## Endpoint

```
POST /api/collections
```

## Request Headers

| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |

## Request Body

The request body must be a JSON object with the following fields:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| name | string | Yes | 2-100 characters | The name of the collection |
| description | string | No | Max 500 characters | A brief description of the collection |

### Request Schema

```typescript
{
  name: string;        // Required: 2-100 characters
  description?: string; // Optional: max 500 characters
}
```

## Response Body

The response body contains the created collection details in a `data` field, along with a `message` field:

| Field | Type | Description |
|-------|------|-------------|
| data | object | Object containing the collection details |
| data.id | string | Unique identifier for the collection |
| data.name | string | Collection name |
| data.description | string | Collection description (empty string if not provided) |
| data.documentCount | number | Number of documents in the collection |
| data.createdAt | string | ISO date format (YYYY-MM-DD) |
| message | string | Success message describing the operation result |

### Response Schema

```typescript
{
  data: {
    id: string;           // Unique identifier for the collection
    name: string;         // Collection name
    description: string;  // Collection description
    documentCount: number; // Number of documents in the collection
    createdAt: string;    // ISO date format (YYYY-MM-DD)
  };
  message: string;        // Success message
}
```

## Example Request

### cURL

```bash
curl -X POST http://localhost:8005/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Documentation",
    "description": "All product manuals and user guides"
  }'
```

### JSON Payload

```json
{
  "name": "Product Documentation",
  "description": "All product manuals and user guides"
}
```

## Example Success Response

**Status Code:** 201 Created

```json
{
  "data": {
    "id": "1",
    "name": "Product Documentation",
    "description": "All product manuals and user guides",
    "documentCount": 0,
    "createdAt": "2024-01-15"
  },
  "message": "Collection created successfully"
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

### 500 Internal Server Error

**Status Code:** 500 Internal Server Error

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred while creating the collection"
}
```

## Status Codes

| Status Code | Description |
|-------------|-------------|
| 201 | Created - Collection successfully created |
| 400 | Bad Request - Invalid request data or validation errors |
| 500 | Internal Server Error - Server encountered an unexpected error |
