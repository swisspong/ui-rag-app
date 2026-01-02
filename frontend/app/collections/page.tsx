"use client"

import * as React from "react"
import {
  MoreHorizontal,
} from "lucide-react"
import Link from "next/link"
import {
  flexRender,
  ColumnDef,
} from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { ArrowUpDown } from "lucide-react"
import { DataTable } from "@/components/ui/data-table"
import { DeleteAction } from "@/components/delete-action"
import { EditAction } from "@/components/edit-action"
import { ActionsDropdown } from "@/components/actions-dropdown"
import { CollectionFormDialog } from "@/components/collections"
import { type CollectionFormData } from "@/components/collections"

// Types
interface Collection {
  id: string
  name: string
  description: string
  documentCount: number
  createdDate: string
}

// Mock data
const initialCollectionsData: Collection[] = [
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

export default function CollectionsPage() {
  const [collectionsData, setCollectionsData] = React.useState<Collection[]>(initialCollectionsData)
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false)
  const [editDialogOpen, setEditDialogOpen] = React.useState(false)
  const [editingCollection, setEditingCollection] = React.useState<Collection | null>(null)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  const handleCreateCollection = async (data: CollectionFormData) => {
    setIsSubmitting(true)
    try {
      console.log("Creating collection:", data)
      // TODO: Replace with actual API call
      
      const newCollection: Collection = {
        id: Date.now().toString(),
        name: data.name,
        description: data.description || "",
        documentCount: 0,
        createdDate: new Date().toISOString().split('T')[0],
      }
      
      setCollectionsData([...collectionsData, newCollection])
      setCreateDialogOpen(false)
    } catch (error) {
      console.error("Error creating collection:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditCollection = async (data: CollectionFormData) => {
    setIsSubmitting(true)
    try {
      console.log("Updating collection:", editingCollection?.id, data)
      // TODO: Replace with actual API call
      
      if (editingCollection) {
        setCollectionsData(
          collectionsData.map((collection) =>
            collection.id === editingCollection.id
              ? { ...collection, name: data.name, description: data.description || "" }
              : collection
          )
        )
      }
      
      setEditDialogOpen(false)
      setEditingCollection(null)
    } catch (error) {
      console.error("Error updating collection:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditClick = (collection: Collection) => {
    setEditingCollection(collection)
    setEditDialogOpen(true)
  }

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
      cell: ({ row }) => {
        const collection = row.original
        return (
          <Link href={`/collections/${collection.id}`} className="font-medium hover:underline">
            {row.getValue("name")}
          </Link>
        )
      },
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

        return (
          <ActionsDropdown>
            <EditAction onClick={() => handleEditClick(collection)} />
            <DeleteAction
              onClick={() => console.log("Delete collection:", collection.id)}
              variant="destructive"
            >
            </DeleteAction>
          </ActionsDropdown>
        )
      },
    },
  ]

  return (
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 lg:p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Collections</h1>
              <p className="text-muted-foreground">
                Manage your document collections
              </p>
            </div>
            <Button onClick={() => setCreateDialogOpen(true)}>Add Collection</Button>
          </div>

          <DataTable
            columns={columns}
            data={collectionsData}
            searchable={true}
            pageSize={5}
          />
        </div>
      </div>

      {/* Create Collection Dialog */}
      <CollectionFormDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
        mode="create"
        onSubmit={handleCreateCollection}
        isSubmitting={isSubmitting}
      />

      {/* Edit Collection Dialog */}
      <CollectionFormDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        mode="edit"
        defaultValues={editingCollection ? {
          name: editingCollection.name,
          description: editingCollection.description,
        } : undefined}
        onSubmit={handleEditCollection}
        isSubmitting={isSubmitting}
      />
    </div>
  )
}
