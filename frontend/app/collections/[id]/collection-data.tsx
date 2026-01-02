"use client"

import * as React from "react"
import {
  flexRender,
  ColumnDef,
} from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ArrowUpDown, MoreHorizontal, Eye, Trash2, Layers } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { FileIcon, FileTextIcon, LayersIcon, ArrowLeftIcon, FileStackIcon } from "lucide-react"
import { StatusBadge } from "@/components/status-badge"

// Types
export interface File {
  id: string
  name: string
  type: string
  size: string
  uploadedDate: string
}

export interface Document {
  id: string
  documentName: string
  filename: string | null
  status: "completed" | "processing" | "pending" | "failed"
  createdDate: string
}

export interface Chunk {
  id: string
  documentName: string
  content: string
  status: "completed" | "processing" | "pending" | "failed"
}

export interface DocumentChunk {
  id: string
  documentName: string
  chunkCount: number
  createdDate: string
}

// Mock data
export const mockFiles: File[] = [
  {
    id: "1",
    name: "product_manual.pdf",
    type: "PDF",
    size: "2.4 MB",
    uploadedDate: "2024-01-15",
  },
  {
    id: "2",
    name: "user_guide.docx",
    type: "DOCX",
    size: "1.2 MB",
    uploadedDate: "2024-01-16",
  },
  {
    id: "3",
    name: "specifications.pdf",
    type: "PDF",
    size: "3.8 MB",
    uploadedDate: "2024-01-17",
  },
  {
    id: "4",
    name: "faq_document.pdf",
    type: "PDF",
    size: "890 KB",
    uploadedDate: "2024-01-18",
  },
  {
    id: "5",
    name: "training_materials.pptx",
    type: "PPTX",
    size: "5.6 MB",
    uploadedDate: "2024-01-19",
  },
]

export const mockDocuments: Document[] = [
  {
    id: "1",
    documentName: "product_manual_v2.pdf",
    filename: "product_manual_v2.pdf",
    status: "completed",
    createdDate: "2024-01-15",
  },
  {
    id: "2",
    documentName: "user_guide_getting_started.pdf",
    filename: "user_guide_getting_started.pdf",
    status: "completed",
    createdDate: "2024-01-16",
  },
  {
    id: "3",
    documentName: "technical_specs.pdf",
    filename: null,
    status: "processing",
    createdDate: "2024-01-17",
  },
  {
    id: "4",
    documentName: "faq_troubleshooting.pdf",
    filename: "faq_troubleshooting.pdf",
    status: "completed",
    createdDate: "2024-01-18",
  },
  {
    id: "5",
    documentName: "training_materials.pdf",
    filename: null,
    status: "pending",
    createdDate: "2024-01-19",
  },
]

export const mockChunks: Chunk[] = [
  {
    id: "1",
    documentName: "product_manual_v2.pdf",
    content: "This product manual provides comprehensive instructions for using our product...",
    status: "completed",
  },
  {
    id: "2",
    documentName: "product_manual_v2.pdf",
    content: "Chapter 1: Introduction. Welcome to our product. This section covers basic setup...",
    status: "completed",
  },
  {
    id: "3",
    documentName: "user_guide_getting_started.pdf",
    content: "Getting Started Guide. This guide will help you understand the basics...",
    status: "processing",
  },
  {
    id: "4",
    documentName: "user_guide_getting_started.pdf",
    content: "Step 1: Installation. Follow these steps to install the software...",
    status: "pending",
  },
  {
    id: "5",
    documentName: "technical_specs.pdf",
    content: "Technical Specifications Document. This document contains detailed specs...",
    status: "failed",
  },
]

export const mockDocumentChunks: DocumentChunk[] = [
  {
    id: "1",
    documentName: "product_manual_v2.pdf",
    chunkCount: 15,
    createdDate: "2024-01-15",
  },
  {
    id: "2",
    documentName: "user_guide_getting_started.pdf",
    chunkCount: 12,
    createdDate: "2024-01-16",
  },
  {
    id: "3",
    documentName: "technical_specs.pdf",
    chunkCount: 8,
    createdDate: "2024-01-17",
  },
  {
    id: "4",
    documentName: "faq_troubleshooting.pdf",
    chunkCount: 20,
    createdDate: "2024-01-18",
  },
  {
    id: "5",
    documentName: "training_materials.pdf",
    chunkCount: 0,
    createdDate: "2024-01-19",
  },
]

// Column definitions for Files
export const fileColumns: ColumnDef<File>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => (
      <div className="font-medium">{row.getValue("name")}</div>
    ),
  },
  {
    accessorKey: "type",
    header: "Type",
    cell: ({ row }) => <div>{row.getValue("type")}</div>,
  },
  {
    accessorKey: "size",
    header: "Size",
    cell: ({ row }) => <div>{row.getValue("size")}</div>,
  },
  {
    accessorKey: "uploadedDate",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Uploaded Date
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("uploadedDate")}</div>,
  },
  {
    id: "actions",
    header: "Action",
    cell: ({ row }) => {
      const file = row.original
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              View
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

// Column definitions for Documents
export const documentColumns: ColumnDef<Document>[] = [
  {
    accessorKey: "documentName",
    header: "Document Name",
    cell: ({ row }) => <div>{row.getValue("documentName")}</div>,
  },
  {
    accessorKey: "filename",
    header: "Filename",
    cell: ({ row }) => {
      const filename = row.getValue("filename") as string | null
      if (!filename) {
        return (
          <span className="px-2 py-0.5 rounded-md bg-muted text-muted-foreground text-xs italic font-medium">
            N/A
          </span>
        )
      }
      return <div>{filename}</div>
    },
  },
  {
    accessorKey: "status",
    header: "OCR Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as "completed" | "processing" | "pending" | "failed"
      return <StatusBadge status={status} />
    },
  },
  {
    id: "actions",
    header: "Action",
    cell: ({ row }) => {
      const document = row.original
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              View
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Layers className="mr-2 h-4 w-4" />
              Chunking
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

// Column definitions for Chunks
export const chunkColumns: ColumnDef<Chunk>[] = [
  {
    accessorKey: "documentName",
    header: "Document",
    cell: ({ row }) => <div className="font-medium">{row.getValue("documentName")}</div>,
  },
  {
    accessorKey: "content",
    header: "Content",
    cell: ({ row }) => (
      <div className="max-w-md truncate">{row.getValue("content")}</div>
    ),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as "completed" | "processing" | "pending" | "failed"
      return <StatusBadge status={status} />
    },
  },
  {
    id: "actions",
    header: "Action",
    cell: ({ row }) => {
      const chunk = row.original
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              View
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

// Column definitions for Document Chunks
export const documentChunkColumns: ColumnDef<DocumentChunk>[] = [
  {
    accessorKey: "documentName",
    header: "Document Name",
    cell: ({ row }) => <div className="font-medium">{row.getValue("documentName")}</div>,
  },
  {
    accessorKey: "chunkCount",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Chunk Count
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("chunkCount")}</div>,
  },
  {
    accessorKey: "createdDate",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 font-medium"
        >
          Created Date
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("createdDate")}</div>,
  },
  {
    id: "actions",
    header: "Action",
    cell: ({ row }) => {
      const documentChunk = row.original
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              View Chunks
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Eye className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

// Collection Tabs Navigation Component
export function CollectionTabs({ collectionId }: { collectionId: string }) {
  const pathname = usePathname()
  
  const getTabClassName = (path: string) => {
    const isActive = pathname === `/collections/${collectionId}${path}`
    return `flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
      isActive 
        ? "bg-primary text-primary-foreground" 
        : "hover:bg-muted"
    }`
  }

  return (
    <div className="grid w-full grid-cols-4 bg-muted rounded-lg p-1">
      <Link
        href={`/collections/${collectionId}/files`}
        className={getTabClassName("/files")}
      >
        <FileIcon className="h-4 w-4" />
        Files
      </Link>
      <Link
        href={`/collections/${collectionId}/documents`}
        className={getTabClassName("/documents")}
      >
        <FileTextIcon className="h-4 w-4" />
        Documents
      </Link>
      <Link
        href={`/collections/${collectionId}/additional-chunks`}
        className={getTabClassName("/additional-chunks")}
      >
        <LayersIcon className="h-4 w-4" />
        Additional Chunks
      </Link>
      <Link
        href={`/collections/${collectionId}/document-chunk`}
        className={getTabClassName("/document-chunk")}
      >
        <FileStackIcon className="h-4 w-4" />
        Document Chunk
      </Link>
    </div>
  )
}

// Collection Header Component
export function CollectionHeader({ 
  collectionId,
  name,
  description 
}: { 
  collectionId: string
  name: string
  description: string 
}) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <Link href="/collections">
          <Button
            variant="ghost"
            size="icon-sm"
            className="h-8 w-8"
          >
            <ArrowLeftIcon className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <FileTextIcon className="h-6 w-6" />
        </div>
        <div className="flex flex-col flex-1 min-w-0">
          <h1 className="text-2xl font-bold tracking-tight">{name}</h1>
          <p className="text-muted-foreground">{description}</p>
        </div>
      </div>
      <CollectionTabs collectionId={collectionId} />
    </div>
  )
}
