"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import { type Collection } from "@/lib/types/collection.types"

interface UseCollectionsResult {
  collections: Collection[]
  isLoading: boolean
  error: string | null
  refetch: (showLoading?: boolean) => Promise<void>
}

interface GetCollectionsParams {
  page?: number
  limit?: number
  search?: string
  sortBy?: 'name' | 'createdAt' | 'fileCount'
  sortOrder?: 'asc' | 'desc'
}

export function useCollections(params?: GetCollectionsParams): UseCollectionsResult {
  const [collections, setCollections] = React.useState<Collection[]>([])
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  const fetchCollections = React.useCallback(async (showLoading: boolean = true) => {
    if (showLoading) {
      setIsLoading(true)
    }
    try {
      const response = await collectionService.getCollections(params || {})
      
      // Validate that response.data exists and is an array
      if (!response.data) {
        console.error("Response data is null or undefined")
        const errorMessage = "Invalid API response: no data received"
        setError(errorMessage)
        toast.error(errorMessage)
        setCollections([])
        return
      }
      
      if (!Array.isArray(response.data)) {
        console.error("Response data is not an array:", response.data)
        const errorMessage = "Invalid API response: data is not an array"
        setError(errorMessage)
        toast.error(errorMessage)
        setCollections([])
        return
      }
      
      setCollections(response.data)
      setError(null)
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to fetch collections"
      setError(errorMessage)
      toast.error(errorMessage)
      setCollections([])
    } finally {
      if (showLoading) {
        setIsLoading(false)
      }
    }
  }, [params])

  React.useEffect(() => {
    let isMounted = true

    fetchCollections(true).then(() => {
      if (!isMounted) {
        setIsLoading(false)
      }
    })

    return () => {
      isMounted = false
    }
  }, [fetchCollections])

  return {
    collections,
    isLoading,
    error,
    refetch: fetchCollections,
  }
}
