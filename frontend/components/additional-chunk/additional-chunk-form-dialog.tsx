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
import { AdditionalChunkForm } from "./additional-chunk-form"
import { type AdditionalChunkData } from "./additional-chunk-schema"

interface AdditionalChunkFormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: AdditionalChunkData) => void | Promise<void>
  isLoading?: boolean
}

export function AdditionalChunkFormDialog({
  open,
  onOpenChange,
  onSubmit,
  isLoading = false,
}: AdditionalChunkFormDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Add Additional Chunk</DialogTitle>
          <DialogDescription>
            Add content and metadata to create a new chunk for the collection
          </DialogDescription>
        </DialogHeader>
        <AdditionalChunkForm onSubmit={onSubmit} isLoading={isLoading} />
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
            form="additional-chunk-form"
            disabled={isLoading}
          >
            {isLoading ? "Saving..." : "Save Changes"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
