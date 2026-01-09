"use client"

import * as React from "react"
import { useSearchParams, useRouter, usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  documentChunkColumns
} from "../collection-data"
import {
  DocumentChunkFormDialog,
  type DocumentChunkFormValues
} from "@/components/document-chunk"
import { toast } from "sonner"
import { useCollection } from "@/lib/hooks/useCollection"
import { useGetCollectionDocuments, useGetDocumentChunks } from "@/lib/hooks/api"

export default function DocumentChunkPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  // URL Params state
  const currentPage = Number(searchParams.get("page")) || 1
  const search = searchParams.get("search") || ""

  const queryParams = React.useMemo(() => ({
    page: currentPage,
    limit: 10,
    search
  }), [currentPage, search])

  // Data fetching
  const { collection, isLoading: isCollectionLoading, error: collectionError } = useCollection(id)
  const { data: documentChunks, isLoading: isChunksLoading, metadata } = useGetDocumentChunks(id, queryParams)
  const { data: documents } = useGetCollectionDocuments(id, { select: true })

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
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

  const handleAddDocumentChunk = async (data: DocumentChunkFormValues) => {
    console.log("Submitted document chunk data:", data)
    setIsSubmitting(true)

    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 1000))

    setIsSubmitting(false)
    setIsDialogOpen(false)
    toast.success("Successfully added document chunk for document ID: " + data.documentId)
  }

  // Show loading state
  if (isCollectionLoading || isChunksLoading) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            <div className="flex items-center justify-center h-64">
              <p className="text-muted-foreground">Loading...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Show error state
  if (collectionError) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <p className="text-destructive font-medium">Error loading collection</p>
                <p className="text-muted-foreground mt-2">{collectionError}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Show content when collection is loaded
  if (!collection) {
    return null
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 lg:p-6 space-y-6">
          {/* Collection Header with Tabs */}
          <CollectionHeader
            collectionId={id}
            name={collection.name}
            description={collection.description}
          />

          {/* Document Chunks Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Document Chunks</h2>
                <p className="text-muted-foreground">
                  Manage document chunking status and view chunks
                </p>
              </div>
              <Button onClick={() => setIsDialogOpen(true)}>Chunk Document</Button>
            </div>
            <DataTable
              columns={documentChunkColumns}
              data={documentChunks}
              searchable={true}
              search={search}
              onFilterChange={handleFilterChange}
              onPageChange={handlePageChange}
              currentPage={currentPage}
              totalPages={metadata ? Math.ceil(metadata.total / metadata.limit) : 1}
              pageSize={queryParams.limit}
            />
          </div>
        </div>
      </div>

      <DocumentChunkFormDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        onSubmit={handleAddDocumentChunk}
        isLoading={isSubmitting}
        documents={documents.map(d => ({ id: d.id, name: d.name }))}
      />
    </div>
  )
}
