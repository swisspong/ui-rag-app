"use client"

import * as React from "react"
import { toast } from "sonner"
import { documentChunkService, ApiError } from "@/lib/services"
import type {
    DocumentChunk,
    DocumentChunkMetadata,
    GetDocumentChunksParams,
} from "@/lib/types"

interface UseGetDocumentChunksResult {
    data: DocumentChunk[]
    metadata: DocumentChunkMetadata | null
    isLoading: boolean
    error: string | null
    refetch: () => Promise<void>
}

/**
 * Hook for fetching document chunks in a collection
 * 
 * @param collectionId - The collection ID
 * @param params - Query parameters for filtering and pagination
 * @returns Object containing data, metadata, loading state, error, and refetch function
 */
export function useGetDocumentChunks(
    collectionId: string,
    params: GetDocumentChunksParams = {}
): UseGetDocumentChunksResult {
    const [data, setData] = React.useState<DocumentChunk[]>([])
    const [metadata, setMetadata] = React.useState<DocumentChunkMetadata | null>(null)
    const [isLoading, setIsLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)

    const fetchDocumentChunks = React.useCallback(async () => {
        if (!collectionId) return

        try {
            const response = await documentChunkService.getDocumentChunks(collectionId, params)
            setData(response.data)
            setMetadata(response.metadata)
            setError(null)
        } catch (err) {
            const errorMessage = err instanceof ApiError
                ? err.message
                : "Failed to fetch document chunks"
            setError(errorMessage)
            toast.error(errorMessage)
        } finally {
            setIsLoading(false)
        }
    }, [collectionId, params.page, params.limit, params.search])

    React.useEffect(() => {
        let isMounted = true

        fetchDocumentChunks().then(() => {
            if (!isMounted) {
                setIsLoading(false)
            }
        })

        return () => {
            isMounted = false
        }
    }, [fetchDocumentChunks])

    return {
        data,
        metadata,
        isLoading,
        error,
        refetch: fetchDocumentChunks,
    }
}

