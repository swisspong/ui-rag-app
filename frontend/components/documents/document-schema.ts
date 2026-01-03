import { z } from "zod"

// Document schema for OCR document creation
export const documentSchema = z.object({
  fileId: z
    .string()
    .min(1, "Please select a file"),
})

// Export inferred TypeScript type
export type DocumentFormData = z.infer<typeof documentSchema>

// Type for file list prop
export interface FileOption {
  id: string
  name: string
}
