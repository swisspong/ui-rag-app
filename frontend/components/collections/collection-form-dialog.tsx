"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { CollectionForm } from "./collection-form"
import { type CollectionFormData } from "./collection-schema"

type FormMode = "create" | "edit"

interface CollectionFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  mode: FormMode
  defaultValues?: Partial<CollectionFormData>
  onSubmit: (data: CollectionFormData) => void | Promise<void>
  isSubmitting?: boolean
}

export function CollectionFormDialog({
  open,
  onOpenChange,
  mode,
  defaultValues,
  onSubmit,
  isSubmitting = false,
}: CollectionFormDialogProps) {
  const title = mode === "create" ? "Create Collection" : "Edit Collection"
  const description =
    mode === "create"
      ? "Create a new collection to organize your documents"
      : "Update the collection details"
  const submitButtonText = mode === "create" ? "Create" : "Save Changes"

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <CollectionForm
          onSubmit={onSubmit}
          defaultValues={defaultValues}
          isSubmitting={isSubmitting}
          submitButtonText={submitButtonText}
        />
      </DialogContent>
    </Dialog>
  )
}
