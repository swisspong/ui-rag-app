# Upload Multiple Files API

Uploads multiple files to a specific collection using multipart/form-data encoding.

## HTTP Method & Endpoint

```
POST /api/collections/{id}/files
```

## Path Parameters

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| id        | string | Yes      | Unique identifier for the collection to upload files to |

## Request Format

- **Content-Type**: `multipart/form-data`
- **Encoding**: multipart/form-data for file uploads

## Form Fields

| Field Name | Type   | Required | Description |
|------------|--------|----------|-------------|
| files      | File[] | Yes      | Array of files to upload (minimum 1 file) |

## File Constraints

| Constraint          | Value/Rule                     |
|---------------------|--------------------------------|
| Maximum file size   | 10 MB per file                |
| Minimum files       | 1 (at least one file required) |
| Accepted extensions | .pdf, .doc, .docx, .txt       |

## Accepted MIME Types

| File Extension | MIME Type                                                                 |
|----------------|---------------------------------------------------------------------------|
| .pdf           | application/pdf                                                          |
| .doc           | application/msword                                                        |
| .docx          | application/vnd.openxmlformats-officedocument.wordprocessingml.document  |
| .txt           | text/plain                                                                |

## Response Body Schema

```typescript
{
  data: {
    uploadedFiles: Array<{
      id: string
      name: string
      size: number
      type: string
      collectionId: string
      uploadedAt: string
    }>
    totalFiles: number
    collectionId: string
  }
  message: string
}
```

### Response Field Details

#### uploadedFiles Array

| Field        | Type   | Description |
|--------------|--------|-------------|
| id           | string | Unique identifier for the uploaded file |
| name         | string | Original filename of the uploaded file |
| size         | number | File size in bytes |
| type         | string | MIME type of the file |
| collectionId | string | ID of the collection the file belongs to |
| uploadedAt   | string | ISO 8601 timestamp of when the file was uploaded |

#### Metadata Fields

| Field        | Type   | Description |
|--------------|--------|-------------|
| totalFiles   | number | Total number of files uploaded in this request |
| collectionId | string | ID of the collection files were uploaded to |
| message      | string | Human-readable message about the operation result |

## Example Request

```bash
curl -X POST http://localhost:3000/api/collections/1/files \
  -F "files=@document1.pdf" \
  -F "files=@document2.docx" \
  -F "files=@notes.txt"
```

## Example Success Response

**Status Code**: 200 OK

```json
{
  "data": {
    "uploadedFiles": [
      {
        "id": "file_001",
        "name": "document1.pdf",
        "size": 1048576,
        "type": "application/pdf",
        "collectionId": "1",
        "uploadedAt": "2024-01-15T10:30:00.000Z"
      },
      {
        "id": "file_002",
        "name": "document2.docx",
        "size": 524288,
        "type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "collectionId": "1",
        "uploadedAt": "2024-01-15T10:30:00.000Z"
      },
      {
        "id": "file_003",
        "name": "notes.txt",
        "size": 1024,
        "type": "text/plain",
        "collectionId": "1",
        "uploadedAt": "2024-01-15T10:30:00.000Z"
      }
    ],
    "totalFiles": 3,
    "collectionId": "1"
  },
  "message": "Files uploaded successfully"
}
```

## Example Error Responses

### 400 Bad Request - No Files Provided

```json
{
  "data": null,
  "message": "No files provided. At least one file is required."
}
```

### 400 Bad Request - File Size Exceeded

```json
{
  "data": null,
  "message": "File 'large_file.pdf' exceeds maximum size of 10 MB."
}
```

### 400 Bad Request - Invalid File Type

```json
{
  "data": null,
  "message": "File 'image.png' has an invalid file type. Accepted types: PDF, DOC, DOCX, TXT."
}
```

### 404 Not Found - Collection Not Found

```json
{
  "data": null,
  "message": "Collection with id '999' not found."
}
```

### 500 Internal Server Error

```json
{
  "data": null,
  "message": "An unexpected error occurred while uploading files. Please try again later."
}
```

## Status Codes

| Status Code | Description                         |
|-------------|-------------------------------------|
| 200         | Files uploaded successfully         |
| 400         | Bad Request - Validation errors      |
| 404         | Not Found - Collection not found    |
| 500         | Internal Server Error               |
