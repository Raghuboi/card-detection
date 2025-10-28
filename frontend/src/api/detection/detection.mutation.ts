import { QueryClient } from '@tanstack/react-query'
import { apiClient } from '@/services/apiClient'

// DTO: Reset Count
type ResetCountResponseDTO = {
  message: string
  running_count: number
  detected_cards: number
}

const resetCount = async () => {
  const response = await apiClient.post<ResetCountResponseDTO>('/api/reset')
  return response.data
}

export const resetCountOptions = (queryClient: QueryClient) => ({
  mutationFn: resetCount,
  onSuccess: () => {
    // Invalidate all detection queries
    queryClient.invalidateQueries({ queryKey: ['detection'] })
  },
})
