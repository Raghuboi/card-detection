---
React Query Patterns - Frontend Architecture

Folder Structure

frontend/src/
├── api/                          # API layer (domain-based)
│   ├── index.ts                 # Barrel exports
│   ├── user/
│   │   ├── index.ts
│   │   ├── user.query.ts        # Query functions
│   │   └── user.mutation.ts     # Mutation functions
│   ├── organization/
│   │   ├── index.ts
│   │   ├── organization.query.ts
│   │   └── organization.mutation.ts
│   └── quiz/
│       ├── index.ts
│       └── quiz.mutation.ts
├── components/
│   ├── ui/                      # shadcn/ui components
│   └── custom/                  # Custom reusable components
├── features/                    # Feature-based components
│   ├── organization/
│   │   ├── cards/
│   │   └── dialogs/
│   └── quiz/
├── routes/                      # TanStack Router file-based routes
├── services/                    # API client & services
├── hooks/                       # Custom React hooks
├── types/                       # TypeScript types
└── utils/                       # Utility functions

---
React Query Patterns

Core Principles

1. No hooks abstraction - Use queryOptions/mutationOptions directly
2. DTOs colocated above functions - Type definitions immediately precede their functions
3. Component-level toast handling - API layer stays pure, components handle UI feedback
4. Domain-based organization - Group by feature (user, organization, quiz)

---
Query Pattern (*.query.ts)

// frontend/src/api/user/user.query.ts

// DTO: Get User
type GetUserResponseDTO = {
  id: string;
  email: string;
  subscription: { /* ... */ } | null;
  organizations: Array<{ /* ... */ }>;
};

const getUser = async () => {
  const response = await apiGatewayClient.get<GetUserResponseDTO>('/user');
  return response.data;
};

export const getUserOptions = () => queryOptions({
  queryKey: ['user', 'profile'],
  queryFn: getUser,
  staleTime: 0,
  retry: false,
});

Key characteristics:
- DTOs defined directly above the function
- Functions are async and return response.data
- Export queryOptions factory function
- Query keys follow pattern: ['domain', 'operation', filters?]

---
Mutation Pattern (*.mutation.ts)

// frontend/src/api/user/user.mutation.ts

// DTO: Login
type LoginRequestDTO = {
  email: string;
  password: string;
};

const login = async (args: LoginRequestDTO) => {
  const response = await apiGatewayClient.post<{ message: string }>('/user/login', args);
  return response.data;
};

export const loginOptions = (queryClient: QueryClient) => ({
  mutationFn: login,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['user'] });
  },
});

Key characteristics:
- Accepts QueryClient parameter for cache invalidation
- Returns mutation options object (not mutationOptions() wrapper)
- onSuccess invalidates related queries
- No toast/UI logic in API layer

---
Component Usage

// frontend/src/routes/_auth/login.tsx

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { loginOptions, getUserOptions } from '@/api';

const LoginPage = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  // Queries - use queryOptions directly
  const user = useQuery(getUserOptions());

  // Mutations - spread options + add component-level handlers
  const login = useMutation({
    ...loginOptions(queryClient),
    onMutate: () => {
      toast.dismiss();
      toast.loading('Signing in...');
    },
    onSuccess: () => {
      toast.success('Signed in!');
      navigate({ to: '/' });
    },
    onError: (error: AxiosError<ServerError>) => {
      const { message, description } = getErrorMessage(error);
      toast.error(message, { description });
    },
  });

  return (
    <form onSubmit={() => login.mutate({ email, password })}>
      {/* ... */}
    </form>
  );
};

Pattern highlights:
- Import from @/api barrel exports
- useQuery receives queryOptions directly
- useMutation spreads API options + adds UI handlers
- Toast notifications at component level
- Error handling uses typed AxiosError<ServerError>

---
Query Key Patterns

// Generic → Specific structure
['user', 'profile']                        // Get current user
['organization', 'list']                   // List organizations
['organization', 'detail', { id }]         // Get specific org
['quiz', 'results', { userId, quizId }]    // Quiz results with filters

Invalidation strategy:
// Invalidate all user queries
queryClient.invalidateQueries({ queryKey: ['user'] });

// Invalidate specific organization
queryClient.invalidateQueries({ queryKey: ['organization', 'detail', { id }] });

---
Advanced Patterns

Conditional queries:
export const getOrganizationOptions = (id?: string | null) => queryOptions({
  queryKey: ['organization', 'detail', { id }],
  queryFn: () => getOrganization(id!),
  enabled: Boolean(id),  // Only fetch if ID exists
});

Prefetching in route loaders:
// frontend/src/routes/organizations.tsx

export const Route = createFileRoute("/organizations")({
  component: OrganizationsPage,
  beforeLoad: async ({ context: { queryClient } }) => {
    await queryClient.fetchQuery({
      ...getUserOptions(),
      staleTime: 5 * 60 * 1000,
      retry: false,
    });
  },
});

Multiple invalidations:
export const joinOrganizationOptions = (queryClient: QueryClient) => ({
  mutationFn: joinOrganization,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['user'] });
    queryClient.invalidateQueries({ queryKey: ['organization'] });
  },
});

---
API Client Setup

Uses Axios client (@/services/apiClient) with typed responses:

// Use generics only when there's a specific DTO
const response = await apiGatewayClient.get<GetUserResponseDTO>('/user');
const response = await apiGatewayClient.post<{ message: string }>('/user/login', data);

// Otherwise omit generics
await apiGatewayClient.delete(`/organization/${id}`);

---
Summary

✅ DO:
- Colocate DTOs directly above functions
- Use queryOptions() for queries, plain objects for mutations
- Handle toasts/navigation in components
- Follow ['domain', 'operation', filters] query key pattern
- Invalidate queries in mutation onSuccess

❌ DON'T:
- Create custom hooks wrapping queries/mutations
- Add toast logic to API layer
- Use placeholders in tool calls
- Batch multiple DTO definitions far from functions

This pattern maximizes type safety, keeps API layer pure, and gives components full control over UI feedback.
