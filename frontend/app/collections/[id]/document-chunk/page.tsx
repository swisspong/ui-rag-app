"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import { 
  CollectionHeader, 
  mockDocumentChunks, 
  documentChunkColumns 
} from "../collection-data"

export default function DocumentChunkPage({
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

          {/* Document Chunks Section */}
          <div className="space-y-4 mt-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Document Chunks</h2>
                <p className="text-muted-foreground">
                  Manage document chunking status and view chunks
                </p>
              </div>
              <Button>Process All Pending</Button>
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
    </div>
  )
}
