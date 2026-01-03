import { z } from "zod"

// Document schema for OCR document creation
export const documentSchema = z.object({
  fileId: z
    .string()
    .min(1, "Please select a file"),
})

// Export inferred TypeScript type
export type DocumentFormData = z.infer<typeof documentSchema>

// Document edit schema for editing document name only
export const documentEditSchema = z.object({
  name: z
    .string()
    .min(1, "Document name is required"),
})

// Export inferred TypeScript type
export type DocumentEditFormData = z.infer<typeof documentEditSchema>

// Type for file list prop
export interface FileOption {
  id: string
  name: string
}
