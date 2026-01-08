import { useState } from 'react'
import { toast } from 'sonner'
import { collectionService } from '@/lib/services/collection.service'
import { ProcessOCRRequest, ProcessOCRResponse } from '@/lib/types/collection.types'

interface UseProcessOCRResult {
    processOCR: (collectionId: string, request: ProcessOCRRequest) => Promise<ProcessOCRResponse>
    isLoading: boolean
    error: string | null
    resetError: () => void
}

export function useProcessOCR(): UseProcessOCRResult {
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const processOCR = async (collectionId: string, request: ProcessOCRRequest) => {
        setIsLoading(true)
        setError(null)
        try {
            const response = await collectionService.processOCR(collectionId, request)
            toast.success("OCR processing started successfully")
            return response
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to process OCR'
            setError(errorMessage)
            toast.error(errorMessage)
            throw err
        } finally {
            setIsLoading(false)
        }
    }

    const resetError = () => setError(null)

    return { processOCR, isLoading, error, resetError }
}
