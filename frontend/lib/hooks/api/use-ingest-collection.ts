"use client"

import { useState } from 'react'
import { toast } from 'sonner'
import { collectionService } from '@/lib/services/collection.service'
import type { IngestCollectionRequest, IngestCollectionResponse } from '@/lib/types/collection.types'

interface UseIngestCollectionResult {
    ingestCollection: (request: IngestCollectionRequest) => Promise<IngestCollectionResponse>
    isLoading: boolean
    error: string | null
    resetError: () => void
}

/**
 * Hook for ingesting a document into a collection
 *
 * @returns Object containing ingestCollection function, loading state, error, and resetError function
 */
export function useIngestCollection(): UseIngestCollectionResult {
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const ingestCollection = async (request: IngestCollectionRequest) => {
        setIsLoading(true)
        setError(null)
        try {
            const response = await collectionService.ingestCollection(request)
            toast.success("Document ingestion started successfully")
            return response
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to ingest collection'
            setError(errorMessage)
            toast.error(errorMessage)
            throw err
        } finally {
            setIsLoading(false)
        }
    }

    const resetError = () => setError(null)

    return { ingestCollection, isLoading, error, resetError }
}
