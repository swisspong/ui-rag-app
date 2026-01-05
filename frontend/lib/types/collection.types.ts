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
