"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldError,
  FieldContent,
} from "@/components/ui/field"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { documentChunkSchema, type DocumentChunkFormValues } from "./document-chunk-schema"

const mockDocuments = [
  { id: "1", name: "Product Manual" },
  { id: "2", name: "User Guide" },
  { id: "3", name: "API Documentation" },
  { id: "4", name: "Technical Specifications" },
]

interface DocumentChunkFormProps {
  onSubmit: (data: DocumentChunkFormValues) => void | Promise<void>
  defaultValues?: Partial<DocumentChunkFormValues>
  isLoading?: boolean
}

export function DocumentChunkForm({
  onSubmit,
  defaultValues,
  isLoading = false,
}: DocumentChunkFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<DocumentChunkFormValues>({
    resolver: zodResolver(documentChunkSchema),
    defaultValues: {
      documentId: defaultValues?.documentId || "",
    },
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} id="document-chunk-form" className="space-y-6">
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="documentId">Select Document *</FieldLabel>
          <FieldContent>
            <Select
              onValueChange={(value) => setValue("documentId", value)}
              defaultValue={defaultValues?.documentId}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a document" />
              </SelectTrigger>
              <SelectContent>
                {mockDocuments.map((document) => (
                  <SelectItem key={document.id} value={document.id}>
                    {document.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FieldContent>
          {errors.documentId && (
            <FieldError errors={[{ message: errors.documentId.message }]} />
          )}
        </Field>
      </FieldGroup>
    </form>
  )
}
