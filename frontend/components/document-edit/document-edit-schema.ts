import { z } from "zod"

// Document edit schema for editing document name only
export const documentEditSchema = z.object({
  name: z
    .string()
    .min(1, "Document name is required"),
})

// Export inferred TypeScript type
export type DocumentEditFormData = z.infer<typeof documentEditSchema>
