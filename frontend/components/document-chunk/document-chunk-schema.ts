import { z } from "zod"

export const documentChunkSchema = z.object({
  documentId: z
    .string()
    .min(1, "Please select a document"),
})

export type DocumentChunkFormValues = z.infer<typeof documentChunkSchema>

export interface DocumentOption {
  id: string
  name: string
}
