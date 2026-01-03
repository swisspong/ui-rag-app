"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockDocuments,
  documentColumns
} from "../collection-data"
import { DocumentFormDialog } from "@/components/documents"
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

  // Mock files data
  const mockFiles: FileOption[] = [
    { id: "file-1", name: "document.pdf" },
    { id: "file-2", name: "scan.jpg" },
    { id: "file-3", name: "report.pdf" },
    { id: "file-4", name: "invoice.png" },
    { id: "file-5", name: "manual.pdf" },
  ]

  // Handle form submission
  const handleSubmit = async (data: DocumentFormData) => {
    setIsSubmitting(true)
    try {
      console.log("Creating document:", data)
      // TODO: Replace with actual API call
      
      // Simulate async operation
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      setIsDialogOpen(false)
    } catch (error) {
      console.error("Error creating document:", error)
    } finally {
      setIsSubmitting(false)
    }
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
              columns={documentColumns}
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
    </div>
  )
}
