"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, File as FileIcon, X, CheckCircle2, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { fileUploadSchema, type FileUploadFormData } from "./file-schema"

interface FileUploadFormProps {
  onSubmit: (data: FileUploadFormData) => void | Promise<void>
  isSubmitting?: boolean
  submitButtonText?: string
}

interface FileWithPreview extends File {
  preview?: string
  id: string
}

export function FileUploadForm({
  onSubmit,
  isSubmitting = false,
  submitButtonText = "Upload Files",
}: FileUploadFormProps) {
  const [files, setFiles] = useState<FileWithPreview[]>([])
  const [uploadProgress, setUploadProgress] = useState<number>(0)

  const {
    setValue,
    setError,
    clearErrors,
    formState: { errors },
  } = useForm<FileUploadFormData>({
    resolver: zodResolver(fileUploadSchema),
    defaultValues: {
      files: [],
    },
  })

  const formatFileSize = (bytes: number | undefined): string => {
    if (bytes === undefined || bytes === null || isNaN(bytes)) return "Unknown size"
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i]
  }

  const getFileIcon = (fileType: string) => {
    return <FileIcon className="h-5 w-5" />
  }

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: any[]) => {
      clearErrors("files")

      if (rejectedFiles.length > 0) {
        rejectedFiles.forEach((rejection: any) => {
          const error = rejection.errors[0]
          setError("files", {
            type: "manual",
            message: `${rejection.file.name}: ${error.message}`,
          })
        })
      }

      // Filter out duplicate files before mapping
      const uniqueNewFiles = acceptedFiles.filter((newFile) =>
        !files.some(existingFile =>
          existingFile.name === newFile.name &&
          existingFile.size === newFile.size
        )
      )

      const newFiles = uniqueNewFiles.map((file) => ({
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
        id: Math.random().toString(36).substring(7),
        preview: URL.createObjectURL(file),
      })) as FileWithPreview[]

      setFiles((prev) => {
        const updatedFiles = [...prev, ...newFiles]
        setValue("files", updatedFiles as any)
        return updatedFiles
      })
    },
    [setValue, setError, clearErrors, files]
  )

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true,
  })

  const removeFile = (fileId: string) => {
    setFiles((prev) => {
      const newFiles = prev.filter((f) => f.id !== fileId)
      setValue("files", newFiles as any)
      return newFiles
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (files.length === 0) {
      setError("files", {
        type: "manual",
        message: "At least one file is required",
      })
      return
    }

    // Mock upload progress
    setUploadProgress(0)
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      await onSubmit({ files: files as any })
      setUploadProgress(100)
      clearInterval(progressInterval)
      
      // Reset form after successful upload
      setTimeout(() => {
        setFiles([])
        setValue("files", [] as any)
        setUploadProgress(0)
      }, 1000)
    } catch (error) {
      clearInterval(progressInterval)
      setUploadProgress(0)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Dropzone Area */}
      <Card>
        <CardHeader>
          <CardTitle>Upload Files</CardTitle>
          <CardDescription>
            Upload PDF, DOC, DOCX, or TXT files (max 10MB each)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            {...getRootProps()}
            className={cn(
              "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
              isDragActive && !isDragReject && "border-primary bg-primary/5",
              isDragReject && "border-destructive bg-destructive/5",
              !isDragActive && "border-muted-foreground/25 hover:border-primary/50"
            )}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-3">
              <Upload className="h-10 w-10 text-muted-foreground" />
              <div className="space-y-1">
                <p className="text-sm font-medium">
                  {isDragActive
                    ? isDragReject
                      ? "File type not supported"
                      : "Drop files here"
                    : "Drag & drop files here, or click to select"}
                </p>
                <p className="text-xs text-muted-foreground">
                  PDF, DOC, DOCX, TXT up to 10MB
                </p>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {errors.files && (
            <div className="mt-3 flex items-center gap-2 text-sm text-destructive">
              <AlertCircle className="h-4 w-4" />
              <span>{errors.files.message}</span>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Selected Files List */}
      {files.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">
              Selected Files ({files.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {files.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center justify-between p-3 rounded-lg border bg-card"
                >
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    <div className="flex-shrink-0 text-muted-foreground">
                      {getFileIcon(file.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {file.name || "Unknown file"}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="flex-shrink-0 h-8 w-8"
                    onClick={() => removeFile(file.id)}
                    disabled={isSubmitting}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Upload Progress */}
      {isSubmitting && uploadProgress > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">Uploading...</span>
                <span className="text-muted-foreground">{uploadProgress}%</span>
              </div>
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Submit Button */}
      <div className="flex justify-end gap-3">
        {files.length > 0 && (
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              setFiles([])
              setValue("files", [] as any)
              clearErrors("files")
            }}
            disabled={isSubmitting}
          >
            Clear All
          </Button>
        )}
        <Button type="submit" disabled={isSubmitting || files.length === 0}>
          {isSubmitting ? (
            <>
              {uploadProgress < 100 ? "Uploading..." : "Complete"}
              {uploadProgress === 100 && (
                <CheckCircle2 className="ml-2 h-4 w-4" />
              )}
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              {submitButtonText}
            </>
          )}
        </Button>
      </div>
    </form>
  )
}
