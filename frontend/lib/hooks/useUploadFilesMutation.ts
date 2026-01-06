"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import type { UploadFilesResponse } from "@/lib/types/collection.types"

interface UseUploadFilesMutationResult {
  mutate: (files: File[]) => Promise<UploadFilesResponse | null>
  mutateAsync: (files: File[]) => Promise<UploadFilesResponse>
  isPending: boolean
  error: string | null
  data: UploadFilesResponse | null
  reset: () => void
}

interface UseUploadFilesMutationOptions {
  onSuccess?: (data: UploadFilesResponse) => void
  onError?: (error: string) => void
  onSettled?: (data: UploadFilesResponse | null, error: string | null) => void
}

/**
 * Mutation-style hook for uploading files to a collection
 * Similar to React Query's useMutation but using native React state
 * 
 * @param collectionId - The ID of the collection to upload files to
 * @param options - Optional callbacks for success, error, and settled states
 * @returns Object containing mutate functions, loading state, error, data, and reset function
 * 
 * @example
 * ```tsx
 * function FileUploader({ collectionId }: { collectionId: string }) {
 *   const { mutate, isPending, error, data, reset } = useUploadFilesMutation(collectionId, {
 *     onSuccess: (data) => {
 *       console.log('Files uploaded:', data.data.uploadedFiles)
 *       // Refresh collections list or perform other actions
 *     },
 *     onError: (error) => {
 *       console.error('Upload failed:', error)
 *     }
 *   })
 *   
 *   const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
 *     const files = Array.from(e.target.files || [])
 *     mutate(files)
 *   }
 *   
 *   return (
 *     <div>
 *       <input 
 *         type="file" 
 *         multiple 
 *         onChange={handleFileChange} 
 *         disabled={isPending}
 *       />
 *       {isPending && <div>Uploading...</div>}
 *       {error && <div className="error">{error}</div>}
 *       {data && (
 *         <div>
 *           <p>Uploaded {data.data.totalFiles} files</p>
 *           <button onClick={reset}>Clear</button>
 *         </div>
 *       )}
 *     </div>
 *   )
 * }
 * ```
 */
export function useUploadFilesMutation(
  collectionId: string,
  options?: UseUploadFilesMutationOptions
): UseUploadFilesMutationResult {
  const [isPending, setIsPending] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [data, setData] = React.useState<UploadFilesResponse | null>(null)

  const mutate = React.useCallback(async (files: File[]): Promise<UploadFilesResponse | null> => {
    if (files.length === 0) {
      const errorMessage = "Please select at least one file to upload"
      toast.error(errorMessage)
      setError(errorMessage)
      options?.onError?.(errorMessage)
      options?.onSettled?.(null, errorMessage)
      return null
    }

    setIsPending(true)
    setError(null)
    setData(null)

    try {
      const response = await collectionService.uploadFiles(collectionId, files)
      
      setData(response)
      setError(null)
      
      toast.success(response.message || "Files uploaded successfully")
      
      options?.onSuccess?.(response)
      options?.onSettled?.(response, null)
      
      return response
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to upload files"
      
      setError(errorMessage)
      toast.error(errorMessage)
      
      options?.onError?.(errorMessage)
      options?.onSettled?.(null, errorMessage)
      
      return null
    } finally {
      setIsPending(false)
    }
  }, [collectionId, options])

  const mutateAsync = React.useCallback(async (files: File[]): Promise<UploadFilesResponse> => {
    const result = await mutate(files)
    
    if (result === null) {
      throw new Error(error || "Upload failed")
    }
    
    return result
  }, [mutate, error])

  const reset = React.useCallback(() => {
    setError(null)
    setData(null)
    setIsPending(false)
  }, [])

  return {
    mutate,
    mutateAsync,
    isPending,
    error,
    data,
    reset,
  }
}
