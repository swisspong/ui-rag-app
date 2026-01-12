"use client"

import * as React from "react"
import { toast } from "sonner"
import { documentService, ApiError } from "@/lib/services"
import type {
    Document,
    DocumentMetadata,
    GetCollectionDocumentsParams,
} from "@/lib/types/document.types"

interface UseGetCollectionDocumentsResult {
    data: Document[]
    metadata: DocumentMetadata | null
    isLoading: boolean
    error: string | null
    refetch: () => Promise<void>
}

/**
 * Hook for fetching documents in a collection
 * 
 * @param collectionId - The collection ID
 * @param params - Query parameters for filtering and pagination
 * @returns Object containing data, metadata, loading state, error, and refetch function
 */
export function useGetCollectionDocuments(
    collectionId: string,
    params: GetCollectionDocumentsParams = {}
): UseGetCollectionDocumentsResult {
    const [data, setData] = React.useState<Document[]>([])
    const [metadata, setMetadata] = React.useState<DocumentMetadata | null>(null)
    const [isLoading, setIsLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)

    // Destructure params to use in dependency array
    // const { page, limit, search, select } = params

    const fetchDocuments = React.useCallback(async () => {
        if (!collectionId) return

        try {
            const response = await documentService.getCollectionDocuments(collectionId, params)

            // Check if response is the standard paginated response
            if ('metadata' in response) {
                setData(response.data)
                setMetadata(response.metadata)
            } else {
                // Handle select=true response if it happens to be called with this hook
                // unexpected but safe handling
                setData(response.data as unknown as Document[])
                setMetadata(null)
            }
            setError(null)
        } catch (err) {
            const errorMessage = err instanceof ApiError
                ? err.message
                : "Failed to fetch documents"
            setError(errorMessage)
            toast.error(errorMessage)
        } finally {
            setIsLoading(false)
        }
    }, [collectionId, params.page, params.limit, params.search, params.select])

    React.useEffect(() => {
        let isMounted = true

        fetchDocuments().then(() => {
            if (!isMounted) {
                setIsLoading(false)
            }
        })

        return () => {
            isMounted = false
        }
    }, [fetchDocuments])

    return {
        data,
        metadata,
        isLoading,
        error,
        refetch: fetchDocuments,
    }
}
