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
