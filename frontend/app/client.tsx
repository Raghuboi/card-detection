import { hydrateRoot } from 'react-dom/client'
import { StartClient } from '@tanstack/start'
import { createRouter, queryClient } from './router'
import { QueryClientProvider } from '@tanstack/react-query'

const router = createRouter()

hydrateRoot(
  document,
  <QueryClientProvider client={queryClient}>
    <StartClient router={router} />
  </QueryClientProvider>
)
