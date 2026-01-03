"use client"

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { DocumentChunkForm } from "./document-chunk-form"
import { type DocumentChunkFormValues } from "./document-chunk-schema"

interface DocumentChunkFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: DocumentChunkFormValues) => void | Promise<void>
  isLoading?: boolean
}

export function DocumentChunkFormDialog({
  open,
  onOpenChange,
  onSubmit,
  isLoading = false,
}: DocumentChunkFormDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Add Document Chunk</DialogTitle>
          <DialogDescription>
            Select a document to add as a chunk to the collection
          </DialogDescription>
        </DialogHeader>
        <DocumentChunkForm onSubmit={onSubmit} isLoading={isLoading} />
        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            form="document-chunk-form"
            disabled={isLoading}
          >
            {isLoading ? "Saving..." : "Save Changes"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
