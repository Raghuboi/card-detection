# Multi-stage build for optimized frontend

# Stage 1: Build stage
FROM node:22-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production stage
FROM node:22-alpine

WORKDIR /app

# Copy built assets and necessary files from builder
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/package*.json ./

# Install only production dependencies
RUN npm ci --production

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
