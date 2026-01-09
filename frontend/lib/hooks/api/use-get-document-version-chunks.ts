"use client"

import * as React from "react"
import { toast } from "sonner"
import { documentChunkService, ApiError } from "@/lib/services"
import type {
    DocumentVersionChunk,
    DocumentChunkMetadata,
    GetDocumentVersionChunksParams,
} from "@/lib/types"

interface UseGetDocumentVersionChunksResult {
    data: DocumentVersionChunk[]
    metadata: DocumentChunkMetadata | null
    isLoading: boolean
    error: string | null
    refetch: () => Promise<void>
}

/**
 * Hook for fetching document chunks for a specific version
 * 
 * @param collectionId - The collection ID
 * @param documentId - The document ID
 * @param version - The document version
 * @param params - Query parameters for filtering and pagination
 * @returns Object containing data, metadata, loading state, error, and refetch function
 */
export function useGetDocumentVersionChunks(
    collectionId: string,
    documentId: string,
    version: number,
    params: GetDocumentVersionChunksParams = {}
): UseGetDocumentVersionChunksResult {
    const [data, setData] = React.useState<DocumentVersionChunk[]>([])
    const [metadata, setMetadata] = React.useState<DocumentChunkMetadata | null>(null)
    const [isLoading, setIsLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)

    // Destructure params to use in dependency array
    const { page, limit, search } = params

    const fetchDocumentVersionChunks = React.useCallback(async () => {
        if (!collectionId || !documentId || version === undefined) return

        setIsLoading(true)
        setError(null)

        try {
            const response = await documentChunkService.getDocumentVersionChunks(
                collectionId,
                documentId,
                version,
                {
                    page,
                    limit,
                    search,
                }
            )

            setData(response.data)
            setMetadata(response.metadata)
        } catch (err) {
            const errorMessage = err instanceof ApiError
                ? err.message
                : "Failed to fetch document version chunks"
            setError(errorMessage)
            toast.error(errorMessage)
        } finally {
            setIsLoading(false)
        }
    }, [collectionId, documentId, version, page, limit, search])

    React.useEffect(() => {
        fetchDocumentVersionChunks()
    }, [fetchDocumentVersionChunks])

    return {
        data,
        metadata,
        isLoading,
        error,
        refetch: fetchDocumentVersionChunks,
    }
}
