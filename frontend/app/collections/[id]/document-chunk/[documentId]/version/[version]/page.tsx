"use client"

import * as React from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import { useRouter, usePathname } from "next/navigation"
import { useGetDocumentVersionChunks } from "@/lib/hooks/api"
import {
  CollectionHeader,
  subChunkColumns,
  type SubChunk
} from "../../../../collection-data"
import { AdditionalChunkFormDialog } from "@/components/additional-chunk"
import { type AdditionalChunkData } from "@/components/additional-chunk"

type FormMode = "create" | "edit"

export default function DocumentChunkDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string; documentId: string; version: string }>
  searchParams: Promise<{ page?: string; limit?: string; search?: string }>
}) {
  const { id, documentId, version } = React.use(params)
  const resolvedSearchParams = React.use(searchParams)
  const router = useRouter()
  const pathname = usePathname()

  // Parse query params
  const page = Number(resolvedSearchParams.page) || 1
  const limit = Number(resolvedSearchParams.limit) || 10
  const search = resolvedSearchParams.search || ""

  // Fetch data
  const {
    data,
    metadata,
    isLoading,
    refetch
  } = useGetDocumentVersionChunks(id, documentId, parseInt(version), {
    page,
    limit,
    search,
  })

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [mode, setMode] = React.useState<FormMode>("create")
  // Using explicit type assertion for editingSubChunk to match the hook data type
  // In a real app we might want to unify these types
  const [editingSubChunk, setEditingSubChunk] = React.useState<any | null>(null)

  const handleAddAdditionalChunk = async (data: AdditionalChunkData) => {
    console.log("Submitted additional chunk data:", data)
    setIsSubmitting(true)

    // Simulate async operation - create hook would be called here
    await new Promise(resolve => setTimeout(resolve, 1000))

    setIsSubmitting(false)
    setIsDialogOpen(false)
    toast.success("Successfully added additional chunk")
    refetch()
  }

  const handleEditAdditionalChunk = async (data: AdditionalChunkData) => {
    console.log("Updated additional chunk data:", data)
    setIsSubmitting(true)

    // Simulate async operation - update hook would be called here
    await new Promise(resolve => setTimeout(resolve, 1000))

    setIsSubmitting(false)
    setIsDialogOpen(false)
    setEditingSubChunk(null)
    toast.success("Successfully updated additional chunk")
    refetch()
  }

  const handleOpenCreateDialog = () => {
    setMode("create")
    setEditingSubChunk(null)
    setIsDialogOpen(true)
  }

  const handleOpenEditDialog = (chunk: any) => {
    setMode("edit")
    setEditingSubChunk(chunk)
    setIsDialogOpen(true)
  }

  const handleSubmit = mode === "create" ? handleAddAdditionalChunk : handleEditAdditionalChunk

  const getDialogDefaultValues = (): Partial<AdditionalChunkData> | undefined => {
    if (mode === "edit" && editingSubChunk) {
      return {
        content: editingSubChunk.content,
        meta: editingSubChunk.meta || {},
      }
    }
    return undefined
  }

  // Handle pagination and search changes
  const createQueryString = React.useCallback(
    (params: Record<string, string | number | null>) => {
      const newSearchParams = new URLSearchParams(resolvedSearchParams as unknown as URLSearchParams)

      for (const [key, value] of Object.entries(params)) {
        if (value === null) {
          newSearchParams.delete(key)
        } else {
          newSearchParams.set(key, String(value))
        }
      }

      return newSearchParams.toString()
    },
    [resolvedSearchParams]
  )

  const handlePageChange = (newPage: number) => {
    router.push(`${pathname}?${createQueryString({ page: newPage })}`)
  }

  const handleSearch = (newSearch: string) => {
    router.push(`${pathname}?${createQueryString({ search: newSearch, page: 1 })}`)
  }

  // Mock collection data - in real app, this would be fetched based on params.id
  const collectionData = {
    id: id,
    name: "Product Documentation",
    description: "All product manuals and user guides",
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 lg:p-6 space-y-6">
          {/* Collection Header with Tabs */}
          <CollectionHeader
            collectionId={id}
            name={collectionData.name}
            description={collectionData.description}
          />

          {/* Document Chunk Detail Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Document Chunk Details</h2>
                <p className="text-muted-foreground">
                  View chunks for document {documentId} version {version}
                </p>
              </div>
              <div className="flex gap-2">
                <Button onClick={handleOpenCreateDialog}>Add Chunk</Button>
                <Button>Process All Pending</Button>
                <Button>Process All Fail</Button>
              </div>
            </div>

            {(isLoading && data.length === 0) ? (
              <div className="flex h-40 items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <DataTable
                columns={subChunkColumns(handleOpenEditDialog)}
                data={data as unknown as SubChunk[]}
                searchable={true}
                onFilterChange={handleSearch}
                search={search}
                totalPages={metadata?.totalPages || 0}
                currentPage={page}
                onPageChange={handlePageChange}
              />
            )}
          </div>
        </div>
      </div>
      <AdditionalChunkFormDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        mode={mode}
        defaultValues={getDialogDefaultValues()}
        onSubmit={handleSubmit}
        isSubmitting={isSubmitting}
      />
    </div>
  )
}
