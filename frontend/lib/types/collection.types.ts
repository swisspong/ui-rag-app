/**
 * Collection entity type
 */
export interface Collection {
  id: string
  name: string
  description: string
  fileCount: number
  createdAt: string
}

/**
 * Collection metadata for pagination
 */
export interface CollectionMetadata {
  page: number
  limit: number
  total: number
  totalPages: number
  hasNextPage: boolean
  hasPreviousPage: boolean
}

/**
 * API response for collection list
 */
export interface CollectionListResponse {
  data: Collection[]
  metadata: CollectionMetadata
  message: string
}

/**
 * Query parameters for fetching collections
 */
export interface GetCollectionsParams {
  page?: number
  limit?: number
  search?: string
  sortBy?: 'name' | 'createdAt' | 'fileCount'
  sortOrder?: 'asc' | 'desc'
}

/**
 * Request body for creating a collection
 */
export interface CreateCollectionRequest {
  name: string
  description?: string
}

/**
 * Response data for creating a collection
 */
export interface CreateCollectionResponse {
  data: {
    id: string
    name: string
    description: string
    documentCount: number
    createdAt: string
  }
  message: string
}

/**
 * Response data for getting a single collection
 */
export interface GetCollectionResponse {
  data: Collection
  message: string
}

/**
 * Uploaded file entity type
 */
export interface UploadedFile {
  id: string
  name: string
  size: number
  type: string
  collectionId: string
  createdAt: string
}

/**
 * Request parameters for uploading files to a collection
 */
export interface UploadFilesRequest {
  collectionId: string
  files: File[]
}

/**
 * Response data for uploading files to a collection
 */
export interface UploadFilesResponse {
  data: {
    uploadedFiles: UploadedFile[]
    totalFiles: number
    collectionId: string
  }
  message: string
}

/**
 * File entity type
 */
export interface CollectionFile {
  id: string
  name: string
  type: string
  size: number
  createdAt: string
}

/**
 * File metadata for pagination
 */
export interface FileMetadata {
  page: number
  limit: number
  total: number
  totalPages: number
  hasNextPage: boolean
  hasPreviousPage: boolean
}

/**
 * API response for files list
 */
export interface GetFilesInCollectionResponse {
  data: CollectionFile[]
  metadata: FileMetadata
  message: string
}

/**
 * Query parameters for fetching files in a collection
 */
export interface GetFilesInCollectionParams {
  collectionId: string
  page?: number
  limit?: number
  search?: string
  sortBy?: 'name' | 'size' | 'createdAt'
  sortOrder?: 'asc' | 'desc'
}
