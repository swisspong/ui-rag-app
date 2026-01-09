import type {
    ChunkDocumentsRequest,
    ChunkDocumentsResponse,
    GetDocumentChunksParams,
    GetDocumentChunksResponse,
    GetDocumentVersionChunksParams,
    GetDocumentVersionChunksResponse,
} from '@/lib/types'
import { ApiError } from './collection.service'


/**
 * Base URL for the API
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8005'

/**
 * Build query string from parameters
 */
function buildQueryString(params: GetDocumentChunksParams): string {
    const queryParams = new URLSearchParams()

    if (params.page !== undefined) {
        queryParams.append('page', params.page.toString())
    }
    if (params.limit !== undefined) {
        queryParams.append('limit', params.limit.toString())
    }
    if (params.search !== undefined && params.search !== '') {
        queryParams.append('search', params.search)
    }

    const queryString = queryParams.toString()
    return queryString ? `?${queryString}` : ''
}

/**
 * Get document chunks in a collection
 * 
 * @param collectionId - The collection ID
 * @param params - Query parameters
 * @returns Promise resolving to the list of document chunks
 */
export async function getDocumentChunks(
    collectionId: string,
    params: GetDocumentChunksParams = {}
): Promise<GetDocumentChunksResponse> {
    const queryString = buildQueryString(params)
    const url = `${API_BASE_URL}/collections/${collectionId}/documentChunks${queryString}`

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store',
        })

        const data = await response.json()

        if (!response.ok) {
            throw new ApiError(
                data.message || 'Failed to fetch document chunks',
                response.status,
                data
            )
        }

        return data
    } catch (error) {
        if (error instanceof ApiError) {
            throw error
        }

        throw new ApiError(
            error instanceof Error ? error.message : 'An unexpected error occurred',
            undefined,
            undefined
        )
    }
}

/**
 * Trigger chunking for documents in a collection
 * 
 * @param collectionId - The collection ID
 * @param request - The chunking request
 * @returns Promise resolving to the response
 */
export async function chunkDocuments(
    collectionId: string,
    request: ChunkDocumentsRequest
): Promise<ChunkDocumentsResponse> {
    const url = `${API_BASE_URL}/collections/${collectionId}/chunking`

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        })

        const data = await response.json()

        if (!response.ok) {
            throw new ApiError(
                data.message || 'Failed to trigger chunking',
                response.status,
                data
            )
        }

        return data
    } catch (error) {
        if (error instanceof ApiError) {
            throw error
        }

        throw new ApiError(
            error instanceof Error ? error.message : 'An unexpected error occurred',
            undefined,
            undefined
        )
    }
}

/**
 * Get document chunks for a specific document version
 * 
 * @param collectionId - The collection ID
 * @param documentId - The document ID
 * @param version - The document version
 * @param params - Query parameters
 * @returns Promise resolving to the list of document version chunks
 */
export async function getDocumentVersionChunks(
    collectionId: string,
    documentId: string,
    version: number,
    params: GetDocumentVersionChunksParams = {}
): Promise<GetDocumentVersionChunksResponse> {
    const queryString = buildQueryString(params)
    const url = `${API_BASE_URL}/collections/${collectionId}/documents/${documentId}/version/${version}/chunks${queryString}`

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store',
        })

        const data = await response.json()

        if (!response.ok) {
            throw new ApiError(
                data.message || 'Failed to fetch document version chunks',
                response.status,
                data
            )
        }

        return data
    } catch (error) {
        if (error instanceof ApiError) {
            throw error
        }

        throw new ApiError(
            error instanceof Error ? error.message : 'An unexpected error occurred',
            undefined,
            undefined
        )
    }
}

/**
 * Document Chunk service object
 */
export const documentChunkService = {
    getDocumentChunks,
    chunkDocuments,
    getDocumentVersionChunks,
}
