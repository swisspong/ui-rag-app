import { z } from "zod"

export const additionalChunkSchema = z.object({
  content: z
    .string()
    .min(1, "Content is required"),
  meta: z
    .string()
    .optional()
    .refine(
      (value) => {
        if (!value || value.trim() === "") return true
        try {
          JSON.parse(value)
          return true
        } catch {
          return false
        }
      },
      { message: "Meta must be valid JSON" }
    ),
})

export type AdditionalChunkFormValues = z.infer<typeof additionalChunkSchema>

// Type for the final output after parsing meta string to object
export type AdditionalChunkData = {
  content: string
  meta: Record<string, any>
}

// Helper function to transform form values to data
export function transformFormValuesToData(values: AdditionalChunkFormValues): AdditionalChunkData {
  return {
    content: values.content,
    meta: (!values.meta || values.meta.trim() === "")
      ? {}
      : JSON.parse(values.meta),
  }
}

// Helper function to transform data to form values
export function transformDataToFormValues(data: AdditionalChunkData): AdditionalChunkFormValues {
  return {
    content: data.content,
    meta: JSON.stringify(data.meta, null, 2),
  }
}
