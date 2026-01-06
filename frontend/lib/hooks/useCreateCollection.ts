"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import type { CreateCollectionRequest, CreateCollectionResponse } from "@/lib/types/collection.types"

interface UseCreateCollectionResult {
  createCollection: (request: CreateCollectionRequest) => Promise<CreateCollectionResponse | null>
  isCreating: boolean
  error: string | null
  data: CreateCollectionResponse | null
  reset: () => void
}

/**
 * Hook for creating a new collection
 * 
 * @returns Object containing createCollection function, loading state, error, data, and reset function
 * 
 * @example
 * ```tsx
 * function CreateCollectionForm() {
 *   const { createCollection, isCreating, error, data, reset } = useCreateCollection()
 *   
 *   const handleSubmit = async (e: React.FormEvent) => {
 *     e.preventDefault()
 *     const formData = new FormData(e.target as HTMLFormElement)
 *     const result = await createCollection({
 *       name: formData.get('name') as string,
 *       description: formData.get('description') as string,
 *     })
 *     
 *     if (result) {
 *       console.log('Collection created:', result.data)
 *     }
 *   }
 *   
 *   return (
 *     <form onSubmit={handleSubmit}>
 *       <input name="name" placeholder="Collection name" />
 *       <textarea name="description" placeholder="Description" />
 *       <button type="submit" disabled={isCreating}>
 *         {isCreating ? 'Creating...' : 'Create Collection'}
 *       </button>
 *       {error && <div className="error">{error}</div>}
 *     </form>
 *   )
 * }
 * ```
 */
export function useCreateCollection(): UseCreateCollectionResult {
  const [isCreating, setIsCreating] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [data, setData] = React.useState<CreateCollectionResponse | null>(null)

  const createCollection = React.useCallback(async (request: CreateCollectionRequest): Promise<CreateCollectionResponse | null> => {
    if (!request.name || request.name.trim() === '') {
      toast.error("Collection name is required")
      return null
    }

    setIsCreating(true)
    setError(null)
    setData(null)

    try {
      const response = await collectionService.createCollection(request)
      
      setData(response)
      setError(null)
      
      toast.success(response.message || "Collection created successfully")
      
      return response
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to create collection"
      
      setError(errorMessage)
      toast.error(errorMessage)
      
      return null
    } finally {
      setIsCreating(false)
    }
  }, [])

  const reset = React.useCallback(() => {
    setError(null)
    setData(null)
    setIsCreating(false)
  }, [])

  return {
    createCollection,
    isCreating,
    error,
    data,
    reset,
  }
}
