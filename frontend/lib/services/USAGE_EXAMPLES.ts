/**
 * Usage examples for the collection service
 * This file demonstrates how to use the collection API service
 */

import { collectionService, ApiError } from '@/lib/services'
import type { GetCollectionsParams } from '@/lib/types'

// Example 1: Fetch all collections with default parameters
async function example1() {
  try {
    const response = await collectionService.getCollections()
    console.log('Collections:', response.data)
    console.log('Metadata:', response.metadata)
    console.log('Message:', response.message)
  } catch (error) {
    console.error('Error:', error)
  }
}

// Example 2: Fetch collections with pagination
async function example2() {
  const params: GetCollectionsParams = {
    page: 1,
    limit: 10,
  }

  const response = await collectionService.getCollections(params)
  console.log(`Page ${response.metadata.page} of ${response.metadata.totalPages}`)
  console.log(`Total collections: ${response.metadata.total}`)
}

// Example 3: Search collections
async function example3() {
  const params: GetCollectionsParams = {
    search: 'product',
    page: 1,
    limit: 10,
  }

  const response = await collectionService.getCollections(params)
  console.log(`Found ${response.metadata.total} collections matching "product"`)
}

// Example 4: Sort collections
async function example4() {
  const params: GetCollectionsParams = {
    sortBy: 'createdAt',
    sortOrder: 'desc',
  }

  const response = await collectionService.getCollections(params)
  console.log('Collections sorted by creation date (newest first)')
}

// Example 5: Combined parameters
async function example5() {
  const params: GetCollectionsParams = {
    page: 2,
    limit: 5,
    search: 'documentation',
    sortBy: 'name',
    sortOrder: 'asc',
  }

  const response = await collectionService.getCollections(params)
  console.log('Filtered and paginated results')
}

// Example 6: Error handling
async function example6() {
  try {
    const params: GetCollectionsParams = {
      sortBy: 'name',
    }

    await collectionService.getCollections(params)
  } catch (error) {
    if (error instanceof ApiError) {
      console.error('API Error:', error.message)
      console.error('Status:', error.status)
      console.error('Data:', error.data)
    } else {
      console.error('Unexpected error:', error)
    }
  }
}

// Example 7: Using in a React component
/*
import { useState, useEffect } from 'react'
import { collectionService, ApiError } from '@/lib/services'
import type { Collection } from '@/lib/types'

function CollectionsList() {
  const [collections, setCollections] = useState<Collection[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchCollections() {
      try {
        setLoading(true)
        const response = await collectionService.getCollections({
          page: 1,
          limit: 10,
        })
        setCollections(response.data)
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message)
        } else {
          setError('An unexpected error occurred')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchCollections()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <ul>
      {collections.map((collection) => (
        <li key={collection.id}>{collection.name}</li>
      ))}
    </ul>
  )
}
*/

// Example 8: Using with React Query (TanStack Query)
/*
import { useQuery } from '@tanstack/react-query'
import { collectionService } from '@/lib/services'
import type { GetCollectionsParams } from '@/lib/types'

function useCollections(params: GetCollectionsParams = {}) {
  return useQuery({
    queryKey: ['collections', params],
    queryFn: () => collectionService.getCollections(params),
  })
}

function CollectionsList() {
  const { data, isLoading, error } = useCollections({
    page: 1,
    limit: 10,
    sortBy: 'createdAt',
    sortOrder: 'desc',
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading collections</div>

  return (
    <ul>
      {data?.data.map((collection) => (
        <li key={collection.id}>{collection.name}</li>
      ))}
    </ul>
  )
}
*/
