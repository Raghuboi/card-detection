import { StrictMode, startTransition } from 'react'
import { hydrateRoot } from 'react-dom/client'
import { StartClient } from '@tanstack/react-start/client'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './router'

startTransition(() => {
  hydrateRoot(
    document,
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <StartClient />
      </QueryClientProvider>
    </StrictMode>,
  )
})
