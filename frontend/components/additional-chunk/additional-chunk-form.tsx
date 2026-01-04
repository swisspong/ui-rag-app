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
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import {
  additionalChunkSchema,
  type AdditionalChunkFormValues,
  type AdditionalChunkData,
  transformFormValuesToData,
  transformDataToFormValues,
} from "./additional-chunk-schema"

interface AdditionalChunkFormProps {
  onSubmit: (data: AdditionalChunkData) => void | Promise<void>
  defaultValues?: Partial<AdditionalChunkData>
  isSubmitting?: boolean
  submitButtonText?: string
}

export function AdditionalChunkForm({
  onSubmit,
  defaultValues,
  isSubmitting = false,
  submitButtonText = "Save",
}: AdditionalChunkFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AdditionalChunkFormValues>({
    resolver: zodResolver(additionalChunkSchema),
    defaultValues: defaultValues ? transformDataToFormValues(defaultValues as AdditionalChunkData) : {
      content: "",
      meta: "{}",
    },
  })

  const handleFormSubmit = (values: AdditionalChunkFormValues) => {
    return onSubmit(transformFormValuesToData(values))
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="content">Content *</FieldLabel>
          <FieldContent>
            <Textarea
              id="content"
              placeholder="Enter the content for this chunk"
              rows={6}
              {...register("content")}
            />
          </FieldContent>
          {errors.content && (
            <FieldError errors={[{ message: errors.content.message }]} />
          )}
        </Field>
        <Field>
          <FieldLabel htmlFor="meta">Meta (JSON)</FieldLabel>
          <FieldContent>
            <Textarea
              id="meta"
              placeholder='{"key": "value"}'
              rows={4}
              {...register("meta")}
            />
          </FieldContent>
          {errors.meta && (
            <FieldError errors={[{ message: String(errors.meta.message) }]} />
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
