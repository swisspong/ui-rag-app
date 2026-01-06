"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import { type Collection } from "@/lib/types/collection.types"

interface UseCollectionResult {
  collection: Collection | null
  isLoading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useCollection(collectionId: string): UseCollectionResult {
  const [collection, setCollection] = React.useState<Collection | null>(null)
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  const fetchCollection = React.useCallback(async () => {
    try {
      const response = await collectionService.getCollection(collectionId)
      setCollection(response.data)
      setError(null)
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to fetch collection"
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }, [collectionId])

  React.useEffect(() => {
    let isMounted = true

    fetchCollection().then(() => {
      if (!isMounted) {
        setIsLoading(false)
      }
    })

    return () => {
      isMounted = false
    }
  }, [fetchCollection])

  return {
    collection,
    isLoading,
    error,
    refetch: fetchCollection,
  }
}
