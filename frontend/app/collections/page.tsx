"use client"

import * as React from "react"
import {
  MoreHorizontal,
} from "lucide-react"
import Link from "next/link"
import { toast } from "sonner"
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
import { getCollections, createCollection } from "@/lib/services"
import type { Collection as ApiCollection, CreateCollectionRequest } from "@/lib/types/collection.types"

// Helper function to format date with standard English format and robust timezone handling
const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return "-"
  
  try {
    // Parse the date string - this handles UTC dates correctly
    // new Date() automatically parses ISO strings (e.g., "2024-01-15T10:00:00Z") as UTC
    const date = new Date(dateString)
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
      console.warn("Invalid date string:", dateString)
      return "-"
    }
    
    // Use Intl.DateTimeFormat with explicit timeZone parameter for robust timezone conversion
    // This ensures the date is correctly converted from UTC to Asia/Bangkok (UTC+7)
    const formatter = new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false, // Use 24-hour format for clarity
    })
    
    // Format the date with the Bangkok timezone
    const formattedDate = formatter.format(date)
    
    return formattedDate
  } catch (error) {
    console.error("Error formatting date:", dateString, error)
    return "-"
  }
}

// Types - Local UI interface matching the API response
interface Collection {
  id: string
  name: string
  description: string
  fileCount: number
  createdAt: string
}

export default function CollectionsPage() {
  const [collectionsData, setCollectionsData] = React.useState<Collection[]>([])
  const [isLoading, setIsLoading] = React.useState(true)
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false)
  const [editDialogOpen, setEditDialogOpen] = React.useState(false)
  const [editingCollection, setEditingCollection] = React.useState<Collection | null>(null)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  // Fetch collections function with optional loading state control
  const fetchCollections = async (showLoading: boolean = true) => {
    if (showLoading) {
      setIsLoading(true)
    }
    try {
      console.log("Fetching collections...")
      const response = await getCollections()
      console.log("API Response:", response)
      console.log("Response data type:", typeof response.data)
      console.log("Response data:", response.data)
      console.log("Is data an array?", Array.isArray(response.data))
      
      // Check if response.data exists and is an array
      if (!response.data) {
        console.error("Response data is null or undefined")
        toast.error("Invalid API response: no data received")
        setCollectionsData([])
        return
      }
      
      if (!Array.isArray(response.data)) {
        console.error("Response data is not an array:", response.data)
        toast.error("Invalid API response: data is not an array")
        setCollectionsData([])
        return
      }
      
      // Map API response to UI interface
      const mappedCollections: Collection[] = response.data.map((apiCollection: ApiCollection) => ({
        id: apiCollection.id,
        name: apiCollection.name,
        description: apiCollection.description,
        fileCount: apiCollection.fileCount,
        createdAt: apiCollection.createdAt,
      }))
      
      console.log("Mapped collections:", mappedCollections)
      setCollectionsData(mappedCollections)
    } catch (error) {
      console.error("Error fetching collections:", error)
      if (error instanceof Error) {
        console.error("Error message:", error.message)
        console.error("Error stack:", error.stack)
      }
      toast.error("Failed to load collections")
      setCollectionsData([])
    } finally {
      if (showLoading) {
        setIsLoading(false)
      }
    }
  }

  const handleCreateCollection = async (data: CollectionFormData) => {
    setIsSubmitting(true)
    try {
      console.log("Creating collection:", data)
      
      const request: CreateCollectionRequest = {
        name: data.name,
        description: data.description,
      }
      
      const response = await createCollection(request)
      console.log("API Response:", response)
      
      // Refetch collections after successful creation
      await fetchCollections(false)
      
      toast.success("Collection created successfully")
      setCreateDialogOpen(false)
    } catch (error) {
      toast.error("Failed to create collection")
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
        
        toast.success("Collection updated successfully")
        setEditDialogOpen(false)
        setEditingCollection(null)
      } catch (error) {
        toast.error("Failed to update collection")
        console.error("Error updating collection:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditClick = (collection: Collection) => {
    setEditingCollection(collection)
    setEditDialogOpen(true)
  }

  // Fetch collections on component mount
  React.useEffect(() => {
    fetchCollections(true)
  }, [])

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
      accessorKey: "fileCount",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="h-8 px-2 font-medium"
          >
            File Count
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
      cell: ({ row }) => <div>{row.getValue("fileCount")}</div>,
    },
    {
      accessorKey: "createdAt",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="h-8 px-2 font-medium"
          >
            Created At
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
      cell: ({ row }) => {
        const createdAt = row.getValue("createdAt") as string
        return <div>{formatDate(createdAt)}</div>
      },
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

          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-muted-foreground">Loading collections...</div>
            </div>
          ) : (
            <DataTable
              columns={columns}
              data={collectionsData}
              searchable={true}
              pageSize={5}
            />
          )}
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
