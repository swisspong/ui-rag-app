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

export default function DocumentsPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  
  // Mock collection data - in real app, this would be fetched based on params.id
  const collectionData = {
    id: id,
    name: "Product Documentation",
    description: "All product manuals and user guides",
  }

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  
  // Edit state
  const [editingDocument, setEditingDocument] = React.useState<{ id: string; name: string } | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = React.useState(false)
  const [isEditSubmitting, setIsEditSubmitting] = React.useState(false)

  // Mock files data
  const mockFiles: FileOption[] = [
    { id: "file-1", name: "document.pdf" },
    { id: "file-2", name: "scan.jpg" },
    { id: "file-3", name: "report.pdf" },
    { id: "file-4", name: "invoice.png" },
    { id: "file-5", name: "manual.pdf" },
  ]

  // Handle form submission for create
  const handleSubmit = async (data: DocumentFormData) => {
    setIsSubmitting(true)
    try {
      console.log("Creating document:", data)
      // TODO: Replace with actual API call
      
      // Simulate async operation
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      toast.success("Document created successfully")
      setIsDialogOpen(false)
    } catch (error) {
      toast.error("Failed to create document")
      console.error("Error creating document:", error)
    } finally {
      setIsSubmitting(false)
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
        files={mockFiles}
        onSubmit={handleSubmit}
        isSubmitting={isSubmitting}
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
