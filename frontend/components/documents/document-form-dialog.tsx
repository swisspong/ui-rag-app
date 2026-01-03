"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DocumentForm } from "./document-form"
import { type DocumentFormData, type FileOption } from "./document-schema"

type FormMode = "create" | "edit"

interface DocumentFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  mode?: FormMode
  files: FileOption[]
  defaultValues?: Partial<DocumentFormData>
  onSubmit: (data: DocumentFormData) => void | Promise<void>
  isSubmitting?: boolean
}

export function DocumentFormDialog({
  open,
  onOpenChange,
  mode = "create",
  files,
  defaultValues,
  onSubmit,
  isSubmitting = false,
}: DocumentFormDialogProps) {
  const title = mode === "create" ? "Create Document" : "Edit Document"
  const description =
    mode === "create"
      ? "Create a new document for OCR processing"
      : "Update the document details"
  const submitButtonText = mode === "create" ? "Create" : "Save Changes"

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DocumentForm
          onSubmit={onSubmit}
          files={files}
          defaultValues={defaultValues}
          isSubmitting={isSubmitting}
          submitButtonText={submitButtonText}
        />
      </DialogContent>
    </Dialog>
  )
}
