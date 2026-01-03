import { z } from "zod"

const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB in bytes
const ACCEPTED_FILE_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
] as const

export const fileSchema = z
  .instanceof(File)
  .refine((file) => file.size <= MAX_FILE_SIZE, {
    message: "File size must be less than 10MB",
  })
  .refine((file) => ACCEPTED_FILE_TYPES.includes(file.type as any), {
    message: "File type must be PDF, DOC, DOCX, or TXT",
  })

export const fileUploadSchema = z.object({
  files: z.array(fileSchema).min(1, "At least one file is required"),
})

export type FileUploadFormData = z.infer<typeof fileUploadSchema>
