"use client"

import * as React from "react"
import Link from "next/link"
import { toast } from "sonner"
import { useSearchParams, useRouter, usePathname } from "next/navigation"
import { ColumnDef } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { ArrowUpDown } from "lucide-react"
import { DataTable } from "@/components/ui/data-table"
import { DeleteAction } from "@/components/delete-action"
import { EditAction } from "@/components/edit-action"
import { ActionsDropdown } from "@/components/actions-dropdown"
import { CollectionFormDialog } from "@/components/collections"
import { type CollectionFormData } from "@/components/collections"
import { createCollection } from "@/lib/services"
import type { CreateCollectionRequest, Collection } from "@/lib/types/collection.types"
import { useCollections } from "@/lib/hooks/useCollections"

// Helper function to format date with standard English format and robust timezone handling
const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return "-"

  try {
    const date = new Date(dateString)

    if (isNaN(date.getTime())) {
      return "-"
    }

    const formatter = new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    })

    return formatter.format(date)
  } catch (error) {
    return "-"
  }
}

export default function CollectionsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()
  const currentPage = Number(searchParams.get("page")) || 1
  const search = searchParams.get("search") || ""

  const params = React.useMemo(() => ({
    page: currentPage,
    limit: 2,
    search
  }), [currentPage, search])

  const { collections, isLoading, error, refetch, metadata } = useCollections(params)

  const [createDialogOpen, setCreateDialogOpen] = React.useState(false)
  const [editDialogOpen, setEditDialogOpen] = React.useState(false)
  const [editingCollection, setEditingCollection] = React.useState<Collection | null>(null)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  const handlePageChange = (pageIndex: number) => {
    const params = new URLSearchParams(searchParams.toString())
    params.set("page", String(pageIndex))
    router.push(`${pathname}?${params.toString()}`, { scroll: false })
  }

  const handleFilterChange = (searchQuery: string) => {
    const params = new URLSearchParams(searchParams.toString())
    if (searchQuery) {
      params.set("search", searchQuery)
    } else {
      params.delete("search")
    }
    params.set("page", "1")
    router.push(`${pathname}?${params.toString()}`, { scroll: false })
  }

  const handleCreateCollection = async (data: CollectionFormData) => {
    setIsSubmitting(true)
    try {
      const request: CreateCollectionRequest = {
        name: data.name,
        description: data.description,
      }

      await createCollection(request)
      await refetch(false)

      toast.success("Collection created successfully")
      setCreateDialogOpen(false)
    } catch (error) {
      toast.error("Failed to create collection")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditCollection = async (data: CollectionFormData) => {
    setIsSubmitting(true)
    try {
      toast.success("Collection updated successfully")
      setEditDialogOpen(false)
      setEditingCollection(null)
    } catch (error) {
      toast.error("Failed to update collection")
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
              onClick={() => {}}
              variant="destructive"
            />
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
            data={collections}
            searchable={true}
            onFilterChange={handleFilterChange}
            onPageChange={handlePageChange}
            currentPage={currentPage}
            totalPages={metadata?.totalPages || 1}
            search={search}
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
