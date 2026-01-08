"use client"

import * as React from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockDocuments,
  documentColumns,
  type Document
} from "../collection-data"
import { DocumentFormDialog } from "@/components/documents"
import { DocumentEditDialog, type DocumentEditFormData } from "@/components/document-edit"
import { type DocumentFormData, type FileOption } from "@/components/documents"
import { useCollection } from "@/lib/hooks/useCollection"
import { useGetFilesSelect, useProcessOCR } from "@/lib/hooks/api"

export default function DocumentsPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const { collection, isLoading, error } = useCollection(id)
  const { data: files, isLoading: filesLoading, error: filesError } = useGetFilesSelect({ collectionId: id })
  const { processOCR, isLoading: isOcrLoading } = useProcessOCR()

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)

  // Edit state
  const [editingDocument, setEditingDocument] = React.useState<{ id: string; name: string } | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = React.useState(false)
  const [isEditSubmitting, setIsEditSubmitting] = React.useState(false)

  // Handle form submission for create
  const handleSubmit = async (data: DocumentFormData) => {
    try {
      console.log("Creating document (OCR):", data)
      await processOCR(id, { collection_file_ids: [data.fileId] })
      setIsDialogOpen(false)
    } catch (error) {
      console.error("Error creating document:", error)
    }
  }

  // Handle form submission for edit
  const handleEditSubmit = async (data: DocumentEditFormData) => {
    setIsEditSubmitting(true)
    try {
      if (editingDocument) {
        console.log("Updating document:", editingDocument.id, data)
        // TODO: Replace with actual API call

        // Simulate async operation
        await new Promise(resolve => setTimeout(resolve, 1500))

        toast.success("Document updated successfully")
        setIsEditDialogOpen(false)
        setEditingDocument(null)
      }
    } catch (error) {
      toast.error("Failed to update document")
      console.error("Error updating document:", error)
    } finally {
      setIsEditSubmitting(false)
    }
  }

  // Handle edit button click
  const handleEdit = (document: Document) => {
    setEditingDocument({ id: document.id, name: document.documentName })
    setIsEditDialogOpen(true)
  }

  // Show loading state
  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            <div className="flex items-center justify-center h-64">
              <p className="text-muted-foreground">Loading collection...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Show error state
  if (error) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <p className="text-destructive font-medium">Error loading collection</p>
                <p className="text-muted-foreground mt-2">{error}</p>
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
              data={mockDocuments}
              searchable={true}
              pageSize={5}
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
