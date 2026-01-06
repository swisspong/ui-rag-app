import type {
  Collection,
  CollectionListResponse,
  CreateCollectionRequest,
  CreateCollectionResponse,
  GetCollectionResponse,
  GetCollectionsParams,
} from '@/lib/types/collection.types'

/**
 * Base URL for the API
 * Can be overridden with NEXT_PUBLIC_API_URL environment variable
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8005'

/**
 * Error class for API errors
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

/**
 * Build query string from parameters
 */
function buildQueryString(params: GetCollectionsParams): string {
  const queryParams = new URLSearchParams()

  if (params.page !== undefined) {
    queryParams.append('page', params.page.toString())
  }
  if (params.limit !== undefined) {
    queryParams.append('limit', params.limit.toString())
  }
  if (params.search !== undefined && params.search !== '') {
    queryParams.append('search', params.search)
  }
  if (params.sortBy !== undefined) {
    queryParams.append('sortBy', params.sortBy)
  }
  if (params.sortOrder !== undefined) {
    queryParams.append('sortOrder', params.sortOrder)
  }

  const queryString = queryParams.toString()
  return queryString ? `?${queryString}` : ''
}

/**
 * Fetch collections from the API
 * 
 * @param params - Query parameters for filtering and pagination
 * @returns Promise resolving to CollectionListResponse
 * @throws ApiError if the request fails
 */
export async function getCollections(
  params: GetCollectionsParams = {}
): Promise<CollectionListResponse> {
  const queryString = buildQueryString(params)
  const url = `${API_BASE_URL}/collections${queryString}`

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Disable caching for fresh data
    })

    const data = await response.json()

    if (!response.ok) {
      throw new ApiError(
        data.message || 'Failed to fetch collections',
        response.status,
        data
      )
    }

    return data as CollectionListResponse
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }

    // Handle network errors or other unexpected errors
    throw new ApiError(
      error instanceof Error ? error.message : 'An unexpected error occurred',
      undefined,
      undefined
    )
  }
}

/**
 * Create a new collection
 *
 * @param request - Collection creation request with name and optional description
 * @returns Promise resolving to CreateCollectionResponse
 * @throws ApiError if the request fails
 */
export async function createCollection(
  request: CreateCollectionRequest
): Promise<CreateCollectionResponse> {
  const url = `${API_BASE_URL}/collections`

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new ApiError(
        data.message || 'Failed to create collection',
        response.status,
        data
      )
    }

    return data as CreateCollectionResponse
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }

    // Handle network errors or other unexpected errors
    throw new ApiError(
      error instanceof Error ? error.message : 'An unexpected error occurred',
      undefined,
      undefined
    )
  }
}

/**
 * Get a single collection by ID
 *
 * @param id - The unique identifier of the collection
 * @returns Promise resolving to GetCollectionResponse
 * @throws ApiError if the request fails
 */
export async function getCollection(
  id: string
): Promise<GetCollectionResponse> {
  const url = `${API_BASE_URL}/collections/${id}`

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Disable caching for fresh data
    })

    const data = await response.json()

    if (!response.ok) {
      throw new ApiError(
        data.message || 'Failed to fetch collection',
        response.status,
        data
      )
    }

    return data as GetCollectionResponse
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }

    // Handle network errors or other unexpected errors
    throw new ApiError(
      error instanceof Error ? error.message : 'An unexpected error occurred',
      undefined,
      undefined
    )
  }
}

/**
 * Collection service object with all collection-related API methods
 */
export const collectionService = {
  getCollections,
  createCollection,
  getCollection,
}
