"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { AdditionalChunkForm } from "./additional-chunk-form"
import { type AdditionalChunkData } from "./additional-chunk-schema"

type FormMode = "create" | "edit"

interface AdditionalChunkFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  mode: FormMode
  defaultValues?: Partial<AdditionalChunkData>
  onSubmit: (data: AdditionalChunkData) => void | Promise<void>
  isSubmitting?: boolean
}

export function AdditionalChunkFormDialog({
  open,
  onOpenChange,
  mode,
  defaultValues,
  onSubmit,
  isSubmitting = false,
}: AdditionalChunkFormDialogProps) {
  const title = mode === "create" ? "Add Additional Chunk" : "Edit Additional Chunk"
  const description =
    mode === "create"
      ? "Add content and metadata to create a new chunk for the collection"
      : "Modify content and metadata for this chunk"
  const submitButtonText = mode === "create" ? "Save Changes" : "Update Changes"

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <AdditionalChunkForm
          onSubmit={onSubmit}
          defaultValues={defaultValues}
          isSubmitting={isSubmitting}
          submitButtonText={submitButtonText}
        />
      </DialogContent>
    </Dialog>
  )
}
