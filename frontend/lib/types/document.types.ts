/**
 * Document entity type
 */
export interface Document {
    id: string
    name: string
    filename: string
    content: string
    status: string
    createdAt: string
}

/**
 * Document metadata for pagination
 */
export interface DocumentMetadata {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNextPage: boolean
    hasPreviousPage: boolean
}

/**
 * Query parameters for fetching documents in a collection
 */
export interface GetCollectionDocumentsParams {
    page?: number
    limit?: number
    search?: string
    select?: boolean
}

/**
 * API response for document list
 */
export interface GetCollectionDocumentsResponse {
    data: Document[]
    metadata: DocumentMetadata
}

/**
 * Simplified document entity for select=true response
 */
export interface DocumentSelect {
    id: string
    name: string
}

/**
 * API response for document list with select=true
 */
export interface GetCollectionDocumentsSelectResponse {
    data: DocumentSelect[]
}
