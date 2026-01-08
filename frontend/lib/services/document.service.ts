import type {
    GetCollectionDocumentsParams,
    GetCollectionDocumentsResponse,
    GetCollectionDocumentsSelectResponse,
} from '@/lib/types'
import { ApiError } from './collection.service'

/**
 * Base URL for the API
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8005'

/**
 * Build query string from parameters
 */
function buildQueryString(params: GetCollectionDocumentsParams): string {
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
    if (params.select !== undefined) {
        queryParams.append('select', params.select.toString())
    }

    const queryString = queryParams.toString()
    return queryString ? `?${queryString}` : ''
}

/**
 * Get documents in a collection
 * 
 * @param collectionId - The collection ID
 * @param params - Query parameters
 * @returns Promise resolving to the list of documents
 */
export async function getCollectionDocuments(
    collectionId: string,
    params: GetCollectionDocumentsParams = {}
): Promise<GetCollectionDocumentsResponse | GetCollectionDocumentsSelectResponse> {
    const queryString = buildQueryString(params)
    const url = `${API_BASE_URL}/collections/${collectionId}/documents${queryString}`

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
                data.message || 'Failed to fetch documents',
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
 * Document service object
 */
export const documentService = {
    getCollectionDocuments,
}
