"use client"

import * as React from "react"
import { Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

export interface DeleteActionProps {
  /** Callback function executed when delete is confirmed */
  onConfirm: () => void
  /** Optional name of the item being deleted for display in the confirmation message */
  itemName?: string
  /** Optional type of the item being deleted for display in the confirmation message */
  itemType?: string
  /** Optional variant for the trigger button */
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  /** Optional size for the trigger button */
  size?: "default" | "sm" | "lg" | "icon"
  /** Optional custom label for the trigger button */
  label?: string
  /** Optional custom title for the confirmation dialog */
  title?: string
  /** Optional custom description for the confirmation dialog */
  description?: string
  /** Optional className for the trigger button */
  className?: string
  /** Optional children to use as custom trigger */
  children?: React.ReactNode
}

export function DeleteAction({
  onConfirm,
  itemName,
  itemType = "item",
  variant = "ghost",
  size = "sm",
  label = "Delete",
  title,
  description,
  className,
  children,
}: DeleteActionProps) {
  const [open, setOpen] = React.useState(false)

  const handleConfirm = () => {
    onConfirm()
    setOpen(false)
  }

  const dialogTitle = title || "Are you sure?"
  const dialogDescription =
    description ||
    (itemName
      ? `This action cannot be undone. This will permanently delete ${itemType} "${itemName}".`
      : `This action cannot be undone. This will permanently delete this ${itemType}.`)

  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      {children ? (
        <AlertDialogTrigger asChild>{children}</AlertDialogTrigger>
      ) : (
        <AlertDialogTrigger asChild>
          <Button
            variant={variant}
            size={size}
            className={className}
          >
            <Trash2 className="h-4 w-4" />
            {label}
          </Button>
        </AlertDialogTrigger>
      )}
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{dialogTitle}</AlertDialogTitle>
          <AlertDialogDescription>
            {dialogDescription}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleConfirm}
            variant="destructive"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
