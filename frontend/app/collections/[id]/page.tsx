"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

export default function CollectionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const router = useRouter()
  
  useEffect(() => {
    const init = async () => {
      const { id } = await params
      router.replace(`/collections/${id}/files`)
    }
    init()
  }, [params, router])

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-muted-foreground">Redirecting...</div>
    </div>
  )
}
