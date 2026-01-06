"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  mockChunks,
  chunkColumns,
  type Chunk
} from "../collection-data"
import {
  AdditionalChunkFormDialog,
  type AdditionalChunkData
} from "@/components/additional-chunk"
import { toast } from "sonner"
import { useCollection } from "@/lib/hooks/useCollection"

type FormMode = "create" | "edit"

export default function ChunksPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const { collection, isLoading, error } = useCollection(id)
  
  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [mode, setMode] = React.useState<FormMode>("create")
  const [editingChunk, setEditingChunk] = React.useState<Chunk | null>(null)

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
    setEditingChunk(null)
    toast.success("Successfully updated additional chunk")
  }

  const handleOpenCreateDialog = () => {
    setMode("create")
    setEditingChunk(null)
    setIsDialogOpen(true)
  }

  const handleOpenEditDialog = (chunk: Chunk) => {
    setMode("edit")
    setEditingChunk(chunk)
    setIsDialogOpen(true)
  }

  const handleSubmit = mode === "create" ? handleAddAdditionalChunk : handleEditAdditionalChunk

  const getDialogDefaultValues = (): Partial<AdditionalChunkData> | undefined => {
    if (mode === "edit" && editingChunk) {
      return {
        content: editingChunk.content,
        meta: {}, // Default empty meta object
      }
    }
    return undefined
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

          {/* Additional Chunks Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Additional Chunks</h2>
                <p className="text-muted-foreground">
                  View additional document chunks for RAG
                </p>
              </div>
              <div className="flex gap-2">
                <Button onClick={handleOpenCreateDialog}>Add Chunk</Button>
                <Button>Process All Pending</Button>
                <Button>Process All Fail</Button>
              </div>
            </div>
            <DataTable
              columns={chunkColumns(handleOpenEditDialog)}
              data={mockChunks}
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
