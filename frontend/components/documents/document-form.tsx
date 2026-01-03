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
import { documentSchema, type DocumentFormData, type FileOption } from "./document-schema"

interface DocumentFormProps {
  onSubmit: (data: DocumentFormData) => void | Promise<void>
  files: FileOption[]
  defaultValues?: Partial<DocumentFormData>
  isSubmitting?: boolean
  submitButtonText?: string
}

export function DocumentForm({
  onSubmit,
  files,
  defaultValues,
  isSubmitting = false,
  submitButtonText = "Save",
}: DocumentFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<DocumentFormData>({
    resolver: zodResolver(documentSchema),
    defaultValues: {
      fileId: defaultValues?.fileId || "",
    },
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="fileId">Select File *</FieldLabel>
          <FieldContent>
            <Select
              onValueChange={(value) => setValue("fileId", value)}
              defaultValue={defaultValues?.fileId}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a file" />
              </SelectTrigger>
              <SelectContent>
                {files.length === 0 ? (
                  <SelectItem value="" disabled>
                    No files available
                  </SelectItem>
                ) : (
                  files.map((file) => (
                    <SelectItem key={file.id} value={file.id}>
                      {file.name}
                    </SelectItem>
                  ))
                )}
              </SelectContent>
            </Select>
          </FieldContent>
          {errors.fileId && (
            <FieldError errors={[{ message: errors.fileId.message }]} />
          )}
        </Field>
      </FieldGroup>

      <div className="flex justify-end">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : submitButtonText}
        </Button>
      </div>
    </form>
  )
}
