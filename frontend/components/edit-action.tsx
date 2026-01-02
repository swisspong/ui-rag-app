"use client"

import * as React from "react"
import { Edit } from "lucide-react"
import { DropdownMenuItem } from "@/components/ui/dropdown-menu"

export interface EditActionProps {
  /** Callback function executed when edit is clicked */
  onClick: () => void
  /** Optional custom label for the menu item */
  label?: string
  /** Optional className for custom styling */
  className?: string
  /** Optional variant for the menu item */
  variant?: "default" | "destructive"
  /** Optional children to use as custom content */
  children?: React.ReactNode
}

export function EditAction({
  onClick,
  label = "Edit",
  className,
  variant,
  children,
}: EditActionProps) {
  return (
    <DropdownMenuItem
      onClick={onClick}
      className={className}
      variant={variant}
    >
      {children || (
        <>
          <Edit className="h-4 w-4 mr-2" />
          {label}
        </>
      )}
    </DropdownMenuItem>
  )
}
