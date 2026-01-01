"use client"

import * as React from "react"
import {
  Edit,
  Trash2,
  MoreHorizontal,
} from "lucide-react"
import {
  flexRender,
  ColumnDef,
} from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ArrowUpDown } from "lucide-react"
import { DataTable } from "@/components/ui/data-table"

// Types
interface Collection {
  id: string
  name: string
  description: string
  documentCount: number
  createdDate: string
}

// Mock data
const collectionsData: Collection[] = [
  {
    id: "1",
    name: "Product Documentation",
    description: "All product manuals and user guides",
    documentCount: 156,
    createdDate: "2024-01-15",
  },
  {
    id: "2",
    name: "Research Papers",
    description: "Academic research and whitepapers",
    documentCount: 89,
    createdDate: "2024-02-20",
  },
  {
    id: "3",
    name: "Customer Support",
    description: "FAQs and support documentation",
    documentCount: 234,
    createdDate: "2024-03-10",
  },
  {
    id: "4",
    name: "Legal Documents",
    description: "Contracts and legal agreements",
    documentCount: 45,
    createdDate: "2024-04-05",
  },
  {
    id: "5",
    name: "Marketing Materials",
    description: "Brochures, presentations, and campaigns",
    documentCount: 178,
    createdDate: "2024-05-12",
  },
  {
    id: "6",
    name: "Technical Specifications",
    description: "Technical docs and API references",
    documentCount: 312,
    createdDate: "2024-06-18",
  },
  {
    id: "7",
    name: "Training Resources",
    description: "Employee training materials",
    documentCount: 67,
    createdDate: "2024-07-22",
  },
  {
    id: "8",
    name: "Project Archives",
    description: "Completed project documentation",
    documentCount: 198,
    createdDate: "2024-08-30",
  },
  {
    id: "9",
    name: "Knowledge Base",
    description: "Internal knowledge sharing",
    documentCount: 423,
    createdDate: "2024-09-14",
  },
  {
    id: "10",
    name: "Compliance Documents",
    description: "Regulatory and compliance materials",
    documentCount: 56,
    createdDate: "2024-10-25",
  },
]

// Column definitions
const columns: ColumnDef<Collection>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => (
      <div className="font-medium">{row.getValue("name")}</div>
    ),
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => (
      <div className="max-w-xs truncate">{row.getValue("description")}</div>
    ),
  },
  {
    accessorKey: "documentCount",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Document Count
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("documentCount")}</div>,
  },
  {
    accessorKey: "createdDate",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Created Date
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("createdDate")}</div>,
  },
  {
    id: "actions",
    header: "Actions",
    cell: ({ row }) => {
      const collection = row.original

      const handleEdit = () => {
        console.log("Edit collection:", collection.id)
        // TODO: Implement edit functionality
      }

      const handleDelete = () => {
        console.log("Delete collection:", collection.id)
        // TODO: Implement delete functionality
      }

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleEdit}>
              <Edit className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem onClick={handleDelete} className="text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

export default function CollectionsPage() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Collections</h1>
          <p className="text-muted-foreground">
            Manage your document collections
          </p>
        </div>
        <Button>Add Collection</Button>
      </div>

      <DataTable
        columns={columns}
        data={collectionsData}
        searchable={true}
        pageSize={5}
      />
    </div>
  )
}
