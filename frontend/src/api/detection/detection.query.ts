import { queryOptions } from '@tanstack/react-query'
import { apiClient } from '@/services/apiClient'

// DTO: Get Detection State
type GetDetectionStateResponseDTO = {
  running_count: number
  total_cards_detected: number
}

const getDetectionState = async () => {
  const response = await apiClient.get<GetDetectionStateResponseDTO>('/api/state')
  return response.data
}

export const getDetectionStateOptions = () =>
  queryOptions({
    queryKey: ['detection', 'state'],
    queryFn: getDetectionState,
    staleTime: 0,
    retry: false,
    refetchInterval: 1000, // Poll every second
  })

// DTO: Detect Cards
export type DetectedCardDTO = {
  name: string
  confidence: number
  rank: string
  suit: string
  bbox: number[]
}

type DetectCardsResponseDTO = {
  cards: DetectedCardDTO[]
  count: number
  total_cards_detected: number
  timestamp: string
}

const detectCards = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post<DetectCardsResponseDTO>(
    '/api/detect',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  )
  return response.data
}

export const detectCardsOptions = () =>
  queryOptions({
    queryKey: ['detection', 'detect'],
    queryFn: () => detectCards(new File([], 'dummy')), // This won't be used directly
    staleTime: 0,
    retry: false,
    enabled: false, // Don't auto-fetch
  })

// Export the function for manual calls
export { detectCards }
