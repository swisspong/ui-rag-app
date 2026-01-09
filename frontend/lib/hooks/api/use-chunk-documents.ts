"use client"

import { useState } from 'react'
import { toast } from 'sonner'
import { documentChunkService } from '@/lib/services/document-chunk.service'
import type { ChunkDocumentsRequest, ChunkDocumentsResponse } from '@/lib/types/document-chunk.types'

interface UseChunkDocumentsResult {
    chunkDocuments: (collectionId: string, request: ChunkDocumentsRequest) => Promise<ChunkDocumentsResponse>
    isLoading: boolean
    error: string | null
    resetError: () => void
}

/**
 * Hook for chunking documents in a collection
 * 
 * @returns Object containing chunkDocuments function, loading state, error, and resetError function
 */
export function useChunkDocuments(): UseChunkDocumentsResult {
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const chunkDocuments = async (collectionId: string, request: ChunkDocumentsRequest) => {
        setIsLoading(true)
        setError(null)
        try {
            const response = await documentChunkService.chunkDocuments(collectionId, request)
            toast.success("Document chunking started successfully")
            return response
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to chunk documents'
            setError(errorMessage)
            toast.error(errorMessage)
            throw err
        } finally {
            setIsLoading(false)
        }
    }

    const resetError = () => setError(null)

    return { chunkDocuments, isLoading, error, resetError }
}
