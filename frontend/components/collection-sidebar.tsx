"use client"

import * as React from "react"
import {
  FileIcon,
  FileTextIcon,
  LayersIcon,
  ArrowLeftIcon,
} from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"

interface CollectionSidebarProps {
  collectionId: string
  collectionName: string
  collectionDescription: string
  activeSection: "files" | "documents" | "chunks"
  onSectionChange: (section: "files" | "documents" | "chunks") => void
  onBack?: () => void
}

export function CollectionSidebar({
  collectionId,
  collectionName,
  collectionDescription,
  activeSection,
  onSectionChange,
  onBack,
}: CollectionSidebarProps) {
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-1">
          {onBack && (
            <Button
              variant="ghost"
              size="icon-sm"
              onClick={onBack}
              className="h-7 w-7"
            >
              <ArrowLeftIcon className="h-4 w-4" />
            </Button>
          )}
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <FileTextIcon className="h-5 w-5" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold">{collectionName}</span>
            <span className="text-xs text-sidebar-foreground/60 line-clamp-1">
              {collectionDescription}
            </span>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Content</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  isActive={activeSection === "files"}
                  onClick={() => onSectionChange("files")}
                >
                  <FileIcon />
                  <span>Files</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton
                  isActive={activeSection === "documents"}
                  onClick={() => onSectionChange("documents")}
                >
                  <FileTextIcon />
                  <span>Documents</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton
                  isActive={activeSection === "chunks"}
                  onClick={() => onSectionChange("chunks")}
                >
                  <LayersIcon />
                  <span>Chunks</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}

