"use client"

import * as React from "react"
import { toast } from "sonner"
import { useSearchParams, useRouter, usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  documentColumns,
} from "../collection-data"
import { DocumentFormDialog } from "@/components/documents"
import { DocumentEditDialog, type DocumentEditFormData } from "@/components/document-edit"
import { type DocumentFormData } from "@/components/documents"
import { useCollection } from "@/lib/hooks/useCollection"
import { useGetFilesSelect, useProcessOCR, useGetCollectionDocuments } from "@/lib/hooks/api"
import type { Document as CollectionDocument } from "@/lib/types/document.types"

export default function DocumentsPage({
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
  const { data: documents, isLoading: isDocumentsLoading, metadata, refetch } = useGetCollectionDocuments(id, queryParams)
  const { data: files } = useGetFilesSelect({ collectionId: id })
  const { processOCR, isLoading: isOcrLoading } = useProcessOCR()

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)

  // Edit state
  const [editingDocument, setEditingDocument] = React.useState<{ id: string; name: string } | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = React.useState(false)
  const [isEditSubmitting, setIsEditSubmitting] = React.useState(false)

  // Pagination & Filter Handlers
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

  // Handle form submission for create
  const handleSubmit = async (data: DocumentFormData) => {
    try {
      await processOCR(id, { collection_file_ids: [data.fileId] })
      await refetch()
      setIsDialogOpen(false)
      toast.success("Document processing started")
    } catch (error) {
      console.error("Error creating document:", error)
      toast.error("Failed to start processing")
    }
  }

  // Handle form submission for edit
  const handleEditSubmit = async () => {
    setIsEditSubmitting(true)
    try {
      if (editingDocument) {
        // TODO: Replace with actual API call
        await new Promise(resolve => setTimeout(resolve, 1500))

        toast.success("Document updated successfully")
        setIsEditDialogOpen(false)
        setEditingDocument(null)
      }
    } catch {
      toast.error("Failed to update document")
    } finally {
      setIsEditSubmitting(false)
    }
  }

  // Handle edit button click
  const handleEdit = (document: CollectionDocument) => {
    setEditingDocument({ id: document.id, name: document.name })
    setIsEditDialogOpen(true)
  }

  // Show loading state
  if (isCollectionLoading || isDocumentsLoading) {
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

          {/* Documents Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Documents</h2>
                <p className="text-muted-foreground">
                  View and manage documents
                </p>
              </div>
              <Button onClick={() => setIsDialogOpen(true)}>Add Document</Button>
            </div>
            <DataTable
              columns={documentColumns(handleEdit)}
              data={documents}
              searchable={true}
              search={search}
              onFilterChange={handleFilterChange}
              onPageChange={handlePageChange}
              currentPage={currentPage}
              totalPages={metadata?.totalPages || 1}
              pageSize={queryParams.limit}
            />
          </div>
        </div>
      </div>

      {/* Document Form Dialog */}
      <DocumentFormDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        mode="create"
        files={files || []}
        onSubmit={handleSubmit}
        isSubmitting={isOcrLoading}
      />

      {/* Document Edit Dialog */}
      {editingDocument && (
        <DocumentEditDialog
          open={isEditDialogOpen}
          onOpenChange={(open) => {
            setIsEditDialogOpen(open)
            if (!open) setEditingDocument(null)
          }}
          documentId={editingDocument.id}
          documentName={editingDocument.name}
          onSubmit={handleEditSubmit}
          isSubmitting={isEditSubmitting}
        />
      )}
    </div>
  )
}
