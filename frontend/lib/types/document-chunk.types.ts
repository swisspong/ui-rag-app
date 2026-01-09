export interface DocumentChunk {
    id: string
    version: number
    name: string
    chunkCount: number
    createdAt: string
}

export interface DocumentChunkMetadata {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNextPage: boolean
    hasPreviousPage: boolean
}

export interface GetDocumentChunksParams {
    page?: number
    limit?: number
    search?: string
}

export interface GetDocumentChunksResponse {
    data: DocumentChunk[]
    metadata: DocumentChunkMetadata
}

export interface ChunkDocumentsRequest {
    document_ids: string[]
}

export interface ChunkDocumentsResponse {
    success: boolean
}

export interface DocumentVersionChunk {
    id: string
    content: string
    meta: Record<string, any>
    status: string
}

export interface GetDocumentVersionChunksParams {
    page?: number
    limit?: number
    search?: string
}

export interface GetDocumentVersionChunksResponse {
    data: DocumentVersionChunk[]
    metadata: DocumentChunkMetadata
}
