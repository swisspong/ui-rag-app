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
    <div className="flex h-[calc(100vh-3.5rem)] overflow-hidden">
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 lg:p-6 space-y-6">
          <div className="text-muted-foreground">Redirecting...</div>
        </div>
      </div>
    </div>
  )
}
