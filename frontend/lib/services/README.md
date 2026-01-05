# API Services

This directory contains API service functions for communicating with the backend.

## Collection Service

The collection service provides methods to interact with the collections API.

### Usage

```typescript
import { collectionService } from '@/lib/services'
import type { GetCollectionsParams } from '@/lib/types'

// Fetch all collections with default parameters
const response = await collectionService.getCollections()

// Fetch collections with custom parameters
const params: GetCollectionsParams = {
  page: 1,
  limit: 10,
  search: 'product',
  sortBy: 'name',
  sortOrder: 'asc'
}

const response = await collectionService.getCollections(params)

console.log(response.data) // Array of collections
console.log(response.metadata) // Pagination metadata
console.log(response.message) // Response message
```

### Environment Variables

The API base URL can be configured using the `NEXT_PUBLIC_API_URL` environment variable:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8005
```

If not set, it defaults to `http://localhost:8005`.

### Error Handling

The service throws `ApiError` for failed requests:

```typescript
import { collectionService, ApiError } from '@/lib/services'

try {
  const response = await collectionService.getCollections()
  // Handle success
} catch (error) {
  if (error instanceof ApiError) {
    console.error('API Error:', error.message)
    console.error('Status:', error.status)
    console.error('Data:', error.data)
  } else {
    console.error('Unexpected error:', error)
  }
}
```

### TypeScript Types

All types are exported from `@/lib/types`:

```typescript
import type {
  Collection,
  CollectionMetadata,
  CollectionListResponse,
  GetCollectionsParams
} from '@/lib/types'
```
