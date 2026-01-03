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
import { Input } from "@/components/ui/input"
import { documentEditSchema, type DocumentEditFormData } from "./document-edit-schema"

interface DocumentEditFormProps {
  onSubmit: (data: DocumentEditFormData) => void | Promise<void>
  defaultValues?: Partial<DocumentEditFormData>
  isSubmitting?: boolean
  submitButtonText?: string
}

export function DocumentEditForm({
  onSubmit,
  defaultValues,
  isSubmitting = false,
  submitButtonText = "Save",
}: DocumentEditFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DocumentEditFormData>({
    resolver: zodResolver(documentEditSchema),
    defaultValues: {
      name: defaultValues?.name || "",
    },
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="name">Document Name *</FieldLabel>
          <FieldContent>
            <Input
              id="name"
              type="text"
              placeholder="Enter document name"
              {...register("name")}
            />
          </FieldContent>
          {errors.name && (
            <FieldError errors={[{ message: errors.name.message }]} />
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
