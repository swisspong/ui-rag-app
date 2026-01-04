"use client"

import * as React from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockSubChunks,
  subChunkColumns,
  type SubChunk
} from "../../collection-data"
import { AdditionalChunkFormDialog } from "@/components/additional-chunk"
import { type AdditionalChunkData } from "@/components/additional-chunk"

type FormMode = "create" | "edit"

export default function DocumentChunkDetailPage({
  params,
}: {
  params: Promise<{ id: string; chunkId: string }>
}) {
  const { id, chunkId } = React.use(params)
  
  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [mode, setMode] = React.useState<FormMode>("create")
  const [editingSubChunk, setEditingSubChunk] = React.useState<SubChunk | null>(null)

  const handleAddAdditionalChunk = async (data: AdditionalChunkData) => {
    console.log("Submitted additional chunk data:", data)
    setIsSubmitting(true)
    
    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    setIsSubmitting(false)
    setIsDialogOpen(false)
    toast.success("Successfully added additional chunk")
  }

  const handleEditAdditionalChunk = async (data: AdditionalChunkData) => {
    console.log("Updated additional chunk data:", data)
    setIsSubmitting(true)
    
    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    setIsSubmitting(false)
    setIsDialogOpen(false)
    setEditingSubChunk(null)
    toast.success("Successfully updated additional chunk")
  }

  const handleOpenCreateDialog = () => {
    setMode("create")
    setEditingSubChunk(null)
    setIsDialogOpen(true)
  }

  const handleOpenEditDialog = (subChunk: SubChunk) => {
    setMode("edit")
    setEditingSubChunk(subChunk)
    setIsDialogOpen(true)
  }

  const handleSubmit = mode === "create" ? handleAddAdditionalChunk : handleEditAdditionalChunk

  const getDialogDefaultValues = (): Partial<AdditionalChunkData> | undefined => {
    if (mode === "edit" && editingSubChunk) {
      return {
        content: editingSubChunk.content,
        meta: {}, // Default empty meta object
      }
    }
    return undefined
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
                  View chunks under document chunk {chunkId}
                </p>
              </div>
              <div className="flex gap-2">
                <Button onClick={handleOpenCreateDialog}>Add Chunk</Button>
                <Button>Process All Pending</Button>
                <Button>Process All Fail</Button>
              </div>
            </div>
            <DataTable
              columns={subChunkColumns(handleOpenEditDialog)}
              data={mockSubChunks}
              searchable={true}
              pageSize={5}
            />
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
