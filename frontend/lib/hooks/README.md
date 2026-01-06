# Collection Hooks Documentation

This directory contains React hooks for managing collection-related operations in the application.

## Available Hooks

### `useCollection`

Hook for fetching a single collection by ID.

**Parameters:**
- `collectionId` (string): The unique identifier of the collection

**Returns:**
- `collection` (Collection | null): The collection data
- `isLoading` (boolean): Loading state
- `error` (string | null): Error message if any
- `refetch` (() => Promise<void>): Function to refetch the collection

**Example:**
```tsx
function CollectionDetail({ collectionId }: { collectionId: string }) {
  const { collection, isLoading, error, refetch } = useCollection(collectionId)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  if (!collection) return <div>Collection not found</div>

  return (
    <div>
      <h1>{collection.name}</h1>
      <p>{collection.description}</p>
      <p>Files: {collection.fileCount}</p>
      <button onClick={refetch}>Refresh</button>
    </div>
  )
}
```

---

### `useCollections`

Hook for fetching a list of collections with pagination and filtering.

**Parameters:**
- `params` (GetCollectionsParams, optional): Query parameters
  - `page` (number): Page number
  - `limit` (number): Items per page
  - `search` (string): Search term
  - `sortBy` ('name' | 'createdAt' | 'fileCount'): Sort field
  - `sortOrder` ('asc' | 'desc'): Sort order

**Returns:**
- `collections` (Collection[]): Array of collections
- `isLoading` (boolean): Loading state
- `error` (string | null): Error message if any
- `refetch` ((showLoading?: boolean) => Promise<void>): Function to refetch collections

**Example:**
```tsx
function CollectionList() {
  const { collections, isLoading, error, refetch } = useCollections({
    page: 1,
    limit: 10,
    sortBy: 'createdAt',
    sortOrder: 'desc'
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <button onClick={() => refetch(true)}>Refresh</button>
      <ul>
        {collections.map(collection => (
          <li key={collection.id}>
            {collection.name} - {collection.fileCount} files
          </li>
        ))}
      </ul>
    </div>
  )
}
```

---

### `useCreateCollection`

Hook for creating a new collection.

**Parameters:** None

**Returns:**
- `createCollection` ((request: CreateCollectionRequest) => Promise<CreateCollectionResponse | null>): Function to create a collection
- `isCreating` (boolean): Loading state
- `error` (string | null): Error message if any
- `data` (CreateCollectionResponse | null): Response data
- `reset` (() => void): Function to reset state

**Example:**
```tsx
function CreateCollectionForm() {
  const { createCollection, isCreating, error, data, reset } = useCreateCollection()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const result = await createCollection({
      name: formData.get('name') as string,
      description: formData.get('description') as string,
    })
    
    if (result) {
      console.log('Collection created:', result.data)
      // Navigate to collection or refresh list
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        name="name" 
        placeholder="Collection name" 
        required 
      />
      <textarea 
        name="description" 
        placeholder="Description" 
      />
      <button type="submit" disabled={isCreating}>
        {isCreating ? 'Creating...' : 'Create Collection'}
      </button>
      {error && <div className="error">{error}</div>}
      {data && (
        <div>
          <p>Collection created successfully!</p>
          <button onClick={reset}>Create Another</button>
        </div>
      )}
    </form>
  )
}
```

---

### `useUploadFiles`

Hook for uploading files to a collection.

**Parameters:**
- `collectionId` (string): The ID of the collection to upload files to

**Returns:**
- `uploadFiles` ((files: File[]) => Promise<UploadFilesResponse | null>): Function to upload files
- `isUploading` (boolean): Loading state
- `error` (string | null): Error message if any
- `data` (UploadFilesResponse | null): Response data
- `reset` (() => void): Function to reset state

**Example:**
```tsx
function FileUploader({ collectionId }: { collectionId: string }) {
  const { uploadFiles, isUploading, error, data, reset } = useUploadFiles(collectionId)
  
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const result = await uploadFiles(files)
    
    if (result) {
      console.log('Uploaded files:', result.data.uploadedFiles)
      console.log('Total files:', result.data.totalFiles)
    }
  }
  
  return (
    <div>
      <input 
        type="file" 
        multiple 
        onChange={handleFileChange} 
        disabled={isUploading}
      />
      {isUploading && <div>Uploading...</div>}
      {error && <div className="error">{error}</div>}
      {data && (
        <div>
          <p>Successfully uploaded {data.data.totalFiles} files</p>
          <ul>
            {data.data.uploadedFiles.map(file => (
              <li key={file.id}>{file.name}</li>
            ))}
          </ul>
          <button onClick={reset}>Upload More</button>
        </div>
      )}
    </div>
  )
}
```

---

### `useUploadFilesMutation`

Mutation-style hook for uploading files to a collection. Similar to React Query's useMutation but using native React state.

**Parameters:**
- `collectionId` (string): The ID of the collection to upload files to
- `options` (UseUploadFilesMutationOptions, optional): Callbacks
  - `onSuccess` ((data: UploadFilesResponse) => void): Called on successful upload
  - `onError` ((error: string) => void): Called on error
  - `onSettled` ((data: UploadFilesResponse | null, error: string | null) => void): Called after completion

**Returns:**
- `mutate` ((files: File[]) => Promise<UploadFilesResponse | null>): Mutation function
- `mutateAsync` ((files: File[]) => Promise<UploadFilesResponse>): Async mutation function that throws on error
- `isPending` (boolean): Loading state
- `error` (string | null): Error message if any
- `data` (UploadFilesResponse | null): Response data
- `reset` (() => void): Function to reset state

**Example:**
```tsx
function FileUploader({ collectionId }: { collectionId: string }) {
  const { mutate, isPending, error, data, reset } = useUploadFilesMutation(collectionId, {
    onSuccess: (data) => {
      console.log('Files uploaded:', data.data.uploadedFiles)
      // Refresh collections list or perform other actions
    },
    onError: (error) => {
      console.error('Upload failed:', error)
    }
  })
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    mutate(files)
  }
  
  return (
    <div>
      <input 
        type="file" 
        multiple 
        onChange={handleFileChange} 
        disabled={isPending}
      />
      {isPending && <div>Uploading...</div>}
      {error && <div className="error">{error}</div>}
      {data && (
        <div>
          <p>Uploaded {data.data.totalFiles} files</p>
          <button onClick={reset}>Clear</button>
        </div>
      )}
    </div>
  )
}
```

**Example with async mutation:**
```tsx
async function handleUpload(files: File[]) {
  try {
    const result = await mutateAsync(files)
    console.log('Upload successful:', result)
  } catch (error) {
    console.error('Upload failed:', error)
  }
}
```

---

## Importing Hooks

You can import hooks individually or from the index file:

```tsx
// Import individual hook
import { useUploadFiles } from '@/lib/hooks/useUploadFiles'

// Import multiple hooks from index
import { 
  useCollection, 
  useCollections, 
  useCreateCollection,
  useUploadFiles,
  useUploadFilesMutation 
} from '@/lib/hooks'
```

---

## Error Handling

All hooks automatically handle errors and display toast notifications using `sonner`. The error state is also available in the returned object for custom error handling.

```tsx
const { error, isUploading } = useUploadFiles(collectionId)

if (error) {
  // Custom error handling
  return <div className="alert alert-error">{error}</div>
}
```

---

## Loading States

All hooks provide loading states that you can use to show loading indicators:

```tsx
const { isLoading } = useCollections()
const { isCreating } = useCreateCollection()
const { isUploading } = useUploadFiles(collectionId)
const { isPending } = useUploadFilesMutation(collectionId)

{isLoading && <Spinner />}
{isCreating && <Spinner />}
{isUploading && <Spinner />}
{isPending && <Spinner />}
```

---

## Best Practices

1. **Use the right hook for the right purpose:**
   - Use `useUploadFiles` for simple file upload scenarios
   - Use `useUploadFilesMutation` when you need callbacks (onSuccess, onError) or want to chain operations

2. **Reset state when needed:**
   - Use the `reset` function to clear error and data states between operations

3. **Handle empty states:**
   - Always check if data exists before rendering

4. **Combine hooks:**
   - You can use multiple hooks in the same component

```tsx
function CollectionManager() {
  const { collections, isLoading: isLoadingList } = useCollections()
  const { createCollection, isCreating } = useCreateCollection()
  const { uploadFiles, isUploading } = useUploadFiles('collection-id')

  // ... component logic
}
```

---

## TypeScript Support

All hooks are fully typed with TypeScript. Type definitions are exported from `@/lib/types/collection.types`:

```tsx
import type { 
  Collection, 
  CreateCollectionRequest, 
  UploadFilesResponse,
  UploadedFile 
} from '@/lib/types/collection.types'
```
