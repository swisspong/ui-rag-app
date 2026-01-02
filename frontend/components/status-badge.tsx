import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const statusBadgeVariants = cva(
  "px-2 py-1 rounded-full text-xs font-medium inline-flex items-center",
  {
    variants: {
      status: {
        completed: "bg-green-500/10 text-green-500 hover:bg-green-500/20",
        processing: "bg-blue-500/10 text-blue-500 hover:bg-blue-500/20",
        pending: "bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20",
        failed: "bg-red-500/10 text-red-500 hover:bg-red-500/20",
      },
    },
    defaultVariants: {
      status: "pending",
    },
  }
)

export interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadgeVariants> {
  status: "completed" | "processing" | "pending" | "failed"
  label?: string
}

function StatusBadge({ className, status, label, ...props }: StatusBadgeProps) {
  const displayLabel = label || status.charAt(0).toUpperCase() + status.slice(1)

  return (
    <span
      className={cn(statusBadgeVariants({ status }), className)}
      {...props}
    >
      {displayLabel}
    </span>
  )
}

export { StatusBadge, statusBadgeVariants }
