"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import type {
  FileSelect,
  GetFilesSelectRequest,
  GetFilesSelectResponse,
} from "@/lib/types/collection.types"

interface UseGetFilesSelectResult {
  data: FileSelect[]
  isLoading: boolean
  error: string | null
  refetch: () => Promise<void>
}

/**
 * Hook for fetching files in a collection with select=true (simplified response)
 * 
 * This hook only retrieves id and name fields for each file, without metadata.
 * 
 * @param params - Parameters including collectionId
 * @returns Object containing files array (with id and name only), loading state, error, and refetch function
 * 
 * @example
 * ```tsx
 * function FileSelectList({ collectionId }: { collectionId: string }) {
 *   const { data, isLoading, error, refetch } = useGetFilesSelect({
 *     collectionId,
 *   })
 *   
 *   if (isLoading) return <div>Loading files...</div>
 *   if (error) return <div>Error: {error}</div>
 *   
 *   return (
 *     <div>
 *       <h2>Files ({data.length})</h2>
 *       <ul>
 *         {data.map((file) => (
 *           <li key={file.id}>{file.name}</li>
 *         ))}
 *       </ul>
 *       <button onClick={refetch}>Refresh</button>
 *     </div>
 *   )
 * }
 * ```
 */
export function useGetFilesSelect(params: GetFilesSelectRequest): UseGetFilesSelectResult {
  const [data, setData] = React.useState<FileSelect[]>([])
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  const fetchFiles = React.useCallback(async () => {
    try {
      const response: GetFilesSelectResponse = await collectionService.getFilesSelect(params)
      setData(response.data)
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
  }, [params?.collectionId])

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
  }, [params?.collectionId])

  return {
    data,
    isLoading,
    error,
    refetch: fetchFiles,
  }
}
