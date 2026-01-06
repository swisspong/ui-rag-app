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
  metadata?: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNextPage: boolean
    hasPreviousPage: boolean
  }
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
  const [metadata, setMetadata] = React.useState<UseCollectionsResult['metadata']>(undefined)
  const dependencyKey = JSON.stringify(params);
  React.useEffect(() => {
    let isMounted = true

    const fetchData = async () => {
      if (isMounted) {
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
          setMetadata(undefined)
          return
        }
        
        if (!Array.isArray(response.data)) {
          console.error("Response data is not an array:", response.data)
          const errorMessage = "Invalid API response: data is not an array"
          setError(errorMessage)
          toast.error(errorMessage)
          setCollections([])
          setMetadata(undefined)
          return
        }
        
        if (isMounted) {
          setCollections(response.data)
          setMetadata(response.metadata)
          setError(null)
        }
      } catch (err) {
        const errorMessage = err instanceof ApiError
          ? err.message
          : "Failed to fetch collections"
        if (isMounted) {
          setError(errorMessage)
          toast.error(errorMessage)
          setCollections([])
          setMetadata(undefined)
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      isMounted = false
    }
  // }, [])
  }, [params?.page, params?.limit, params?.search, params?.sortBy, params?.sortOrder])

  const refetch = React.useCallback(async (showLoading: boolean = true) => {
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
        setMetadata(undefined)
        return
      }
      
      if (!Array.isArray(response.data)) {
        console.error("Response data is not an array:", response.data)
        const errorMessage = "Invalid API response: data is not an array"
        setError(errorMessage)
        toast.error(errorMessage)
        setCollections([])
        setMetadata(undefined)
        return
      }
      
      setCollections(response.data)
      setMetadata(response.metadata)
      setError(null)
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to fetch collections"
      setError(errorMessage)
      toast.error(errorMessage)
      setCollections([])
      setMetadata(undefined)
    } finally {
      if (showLoading) {
        setIsLoading(false)
      }
    }
  }, [params?.page, params?.limit, params?.search, params?.sortBy, params?.sortOrder])

  return {
    collections,
    isLoading,
    error,
    refetch,
    metadata,
  }
}
