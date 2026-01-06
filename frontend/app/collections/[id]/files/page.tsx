"use client"

import * as React from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockFiles,
  fileColumns
} from "../collection-data"
import { FileUploadDialog } from "@/components/files/file-upload-dialog"
import { type FileUploadFormData } from "@/components/files/file-schema"
import { useCollection } from "@/lib/hooks/useCollection"

export default function FilesPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const [uploadDialogOpen, setUploadDialogOpen] = React.useState(false)
  const [isUploading, setIsUploading] = React.useState(false)
  const { collection, isLoading, error } = useCollection(id)

  const handleFileUpload = async (data: FileUploadFormData) => {
    setIsUploading(true)
    try {
      // Mock upload - in real app, this would be an API call
      console.log("Uploading files:", data.files)
      await new Promise((resolve) => setTimeout(resolve, 2000))
      console.log("Files uploaded successfully!")
      toast.success("Files uploaded successfully")
      setUploadDialogOpen(false)
    } catch (error) {
      toast.error("Failed to upload files")
      console.error("Error uploading files:", error)
    } finally {
      setIsUploading(false)
    }
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

          {/* Files Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Files</h2>
                <p className="text-muted-foreground">
                  Manage files in this collection
                </p>
              </div>
              <Button onClick={() => setUploadDialogOpen(true)}>
                Upload File
              </Button>
            </div>
            <DataTable
              columns={fileColumns}
              data={mockFiles}
              searchable={true}
              pageSize={5}
            />
          </div>
        </div>
      </div>

      {/* File Upload Dialog */}
      <FileUploadDialog
        open={uploadDialogOpen}
        onOpenChange={setUploadDialogOpen}
        collectionId={id}
        onSubmit={handleFileUpload}
        isSubmitting={isUploading}
      />
    </div>
  )
}
