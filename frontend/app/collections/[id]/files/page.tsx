"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { DataTable } from "@/components/ui/data-table"
import {
  CollectionHeader,
  collectionFileColumns
} from "../collection-data"
import { FileUploadDialog } from "@/components/files/file-upload-dialog"
import { type FileUploadFormData } from "@/components/files/file-schema"
import { useCollection, useUploadFiles, useGetFiles } from "@/lib/hooks"
import { useSearchParams, useRouter, usePathname } from "next/navigation"

export default function FilesPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = React.use(params)
  const [uploadDialogOpen, setUploadDialogOpen] = React.useState(false)
  const { collection, isLoading: isLoadingCollection, error: collectionError } = useCollection(id)
  const { uploadFiles, isUploading } = useUploadFiles(id)
  
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()
  const currentPage = Number(searchParams.get("page")) || 1
  const search = searchParams.get("search") || ""

  const queryParams = React.useMemo(() => ({
    page: currentPage,
    limit: 5,
    search
  }), [currentPage, search])

  const { files, isLoading: isLoadingFiles, error: filesError, refetch, metadata } = useGetFiles({
    collectionId: id,
    ...queryParams
  })

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

  const handleFileUpload = async (data: FileUploadFormData) => {
    const response = await uploadFiles(data.files)
    if (response) {
      setUploadDialogOpen(false)
      // Refetch files after successful upload
      refetch()
    }
  }

  // Show loading state
  if (isLoadingCollection || isLoadingFiles) {
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

  // Show error state for files
  if (filesError && collection) {
    return (
      <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 lg:p-6 space-y-6">
            <CollectionHeader
              collectionId={id}
              name={collection.name}
              description={collection.description}
            />
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <p className="text-destructive font-medium">Error loading files</p>
                <p className="text-muted-foreground mt-2">{filesError}</p>
                <Button onClick={() => refetch()} className="mt-4">
                  Retry
                </Button>
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
              columns={collectionFileColumns}
              data={files}
              searchable={true}
              onFilterChange={handleFilterChange}
              onPageChange={handlePageChange}
              currentPage={currentPage}
              totalPages={metadata?.totalPages || 1}
              search={search}
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
