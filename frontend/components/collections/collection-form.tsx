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
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { collectionSchema, type CollectionFormData } from "./collection-schema"

interface CollectionFormProps {
  onSubmit: (data: CollectionFormData) => void | Promise<void>
  defaultValues?: Partial<CollectionFormData>
  isSubmitting?: boolean
  submitButtonText?: string
}

export function CollectionForm({
  onSubmit,
  defaultValues,
  isSubmitting = false,
  submitButtonText = "Save",
}: CollectionFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CollectionFormData>({
    resolver: zodResolver(collectionSchema),
    defaultValues: {
      name: defaultValues?.name || "",
      description: defaultValues?.description || "",
    },
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="name">Name *</FieldLabel>
          <FieldContent>
            <Input
              id="name"
              placeholder="Enter collection name"
              {...register("name")}
              aria-invalid={errors.name ? "true" : "false"}
            />
          </FieldContent>
          {errors.name && (
            <FieldError errors={[{ message: errors.name.message }]} />
          )}
        </Field>

        <Field>
          <FieldLabel htmlFor="description">Description</FieldLabel>
          <FieldContent>
            <Textarea
              id="description"
              placeholder="Enter collection description (optional)"
              rows={4}
              {...register("description")}
              aria-invalid={errors.description ? "true" : "false"}
            />
          </FieldContent>
          {errors.description && (
            <FieldError errors={[{ message: errors.description.message }]} />
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
