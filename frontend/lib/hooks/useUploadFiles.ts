"use client"

import * as React from "react"
import { toast } from "sonner"
import { collectionService, ApiError } from "@/lib/services"
import type { UploadFilesResponse } from "@/lib/types/collection.types"

interface UseUploadFilesResult {
  uploadFiles: (files: File[]) => Promise<UploadFilesResponse | null>
  isUploading: boolean
  error: string | null
  data: UploadFilesResponse | null
  reset: () => void
}

export function useUploadFiles(collectionId: string): UseUploadFilesResult {
  const [isUploading, setIsUploading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [data, setData] = React.useState<UploadFilesResponse | null>(null)

  const uploadFiles = React.useCallback(async (files: File[]): Promise<UploadFilesResponse | null> => {
    if (files.length === 0) {
      toast.error("Please select at least one file to upload")
      return null
    }

    setIsUploading(true)
    setError(null)
    setData(null)

    try {
      const response = await collectionService.uploadFiles(collectionId, files)
      
      setData(response)
      setError(null)
      
      toast.success(response.message || "Files uploaded successfully")
      
      return response
    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : "Failed to upload files"
      
      setError(errorMessage)
      toast.error(errorMessage)
      
      return null
    } finally {
      setIsUploading(false)
    }
  }, [collectionId])

  const reset = React.useCallback(() => {
    setError(null)
    setData(null)
    setIsUploading(false)
  }, [])

  return {
    uploadFiles,
    isUploading,
    error,
    data,
    reset,
  }
}
