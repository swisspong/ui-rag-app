"use client"

import * as React from "react"
import { useSearchParams } from "next/navigation"

/**
 * A hook that provides stable search params that don't cause infinite re-renders.
 * This is needed because useSearchParams from next/navigation can cause re-renders
 * when used as a dependency in useEffect.
 */
export function useStableSearchParams() {
  const searchParams = useSearchParams()
  
  // Use refs to store the current values
  const pageRef = React.useRef(Number(searchParams.get("page")) || 1)
  const searchRef = React.useRef(searchParams.get("search") || "")
  
  // Update refs when searchParams changes
  React.useEffect(() => {
    pageRef.current = Number(searchParams.get("page")) || 1
    searchRef.current = searchParams.get("search") || ""
  }, [searchParams])
  
  // Return a stable object with the current values
  return React.useMemo(() => ({
    page: pageRef.current,
    search: searchRef.current,
  }), [searchParams])
}
