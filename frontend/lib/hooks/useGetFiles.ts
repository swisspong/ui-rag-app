"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import type {
  CollectionFile,
  FileMetadata,
  GetFilesInCollectionParams,
  GetFilesInCollectionResponse,
} from "@/lib/types/collection.types"

interface UseGetFilesResult {
  files: CollectionFile[]
  metadata: FileMetadata | null
  isLoading: boolean
  error: string | null
  refetch: () => Promise<void>
}

/**
 * Hook for fetching files in a collection
 * 
 * @param params - Parameters including collectionId and optional query parameters
 * @returns Object containing files array, metadata, loading state, error, and refetch function
 * 
 * @example
 * ```tsx
 * function FileList({ collectionId }: { collectionId: string }) {
 *   const { files, metadata, isLoading, error, refetch } = useGetFiles({
 *     collectionId,
 *     page: 1,
 *     limit: 10,
 *   })
 *   
 *   if (isLoading) return <div>Loading files...</div>
 *   if (error) return <div>Error: {error}</div>
 *   
 *   return (
 *     <div>
 *       <h2>Files ({metadata?.total || 0})</h2>
 *       <ul>
 *         {files.map((file) => (
 *           <li key={file.id}>{file.name}</li>
 *         ))}
 *       </ul>
 *       <button onClick={refetch}>Refresh</button>
 *     </div>
 *   )
 * }
 * ```
 */
export function useGetFiles(params: GetFilesInCollectionParams): UseGetFilesResult {
  const [files, setFiles] = React.useState<CollectionFile[]>([])
  const [metadata, setMetadata] = React.useState<FileMetadata | null>(null)
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  const fetchFiles = React.useCallback(async () => {
    try {
      const response: GetFilesInCollectionResponse = await collectionService.getFilesInCollection(params)
      setFiles(response.data)
      setMetadata(response.metadata)
      setError(null)
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to fetch files"
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }, [params?.page,params?.limit])

  React.useEffect(() => {
    let isMounted = true

    fetchFiles().then(() => {
      if (!isMounted) {
        setIsLoading(false)
      }
    })

    return () => {
      isMounted = false
    }
  }, [params?.page,params?.limit])

  return {
    files,
    metadata,
    isLoading,
    error,
    refetch: fetchFiles,
  }
}
