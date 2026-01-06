"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockDocumentChunks,
  documentChunkColumns
} from "../collection-data"
import {
  DocumentChunkFormDialog,
  type DocumentChunkFormValues
} from "@/components/document-chunk"
import { toast } from "sonner"
import { useCollection } from "@/lib/hooks/useCollection"

export default function DocumentChunkPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const { collection, isLoading, error } = useCollection(id)
  
  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

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

          {/* Document Chunks Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Document Chunks</h2>
                <p className="text-muted-foreground">
                  Manage document chunking status and view chunks
                </p>
              </div>
              <Button onClick={() => setIsDialogOpen(true)}>Add Document</Button>
            </div>
            <DataTable
              columns={documentChunkColumns}
              data={mockDocumentChunks}
              searchable={true}
              pageSize={5}
            />
          </div>
        </div>
      </div>
      
      <DocumentChunkFormDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        onSubmit={handleAddDocumentChunk}
        isLoading={isSubmitting}
      />
    </div>
  )
}
