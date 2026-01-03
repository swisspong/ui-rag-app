"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DocumentEditForm } from "./document-edit-form"
import { type DocumentEditFormData } from "./document-edit-schema"

interface DocumentEditDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  documentId: string
  documentName: string
  onSubmit: (data: DocumentEditFormData) => void | Promise<void>
  isSubmitting?: boolean
}

export function DocumentEditDialog({
  open,
  onOpenChange,
  documentId,
  documentName,
  onSubmit,
  isSubmitting = false,
}: DocumentEditDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Edit Document</DialogTitle>
          <DialogDescription>
            Update the document name
          </DialogDescription>
        </DialogHeader>
        <DocumentEditForm
          onSubmit={onSubmit}
          defaultValues={{ name: documentName }}
          isSubmitting={isSubmitting}
          submitButtonText="Save Changes"
        />
      </DialogContent>
    </Dialog>
  )
}
