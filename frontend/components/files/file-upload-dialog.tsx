"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { FileUploadForm } from "./file-upload-form"
import { type FileUploadFormData } from "./file-schema"

interface FileUploadDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  collectionId: string
  onSubmit: (data: FileUploadFormData) => void | Promise<void>
  isSubmitting?: boolean
}

export function FileUploadDialog({
  open,
  onOpenChange,
  collectionId,
  onSubmit,
  isSubmitting = false,
}: FileUploadDialogProps) {
  const handleSubmit = async (data: FileUploadFormData) => {
    // In a real app, you would send collectionId along with the files
    console.log("Uploading files to collection:", collectionId)
    console.log("Files:", data.files)
    await onSubmit(data)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Upload Files</DialogTitle>
          <DialogDescription>
            Upload documents to this collection. Supported formats: PDF, DOC, DOCX, TXT (max 10MB per file)
          </DialogDescription>
        </DialogHeader>
        <FileUploadForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
      </DialogContent>
    </Dialog>
  )
}
