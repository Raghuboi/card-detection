# Development mode - no build step required
FROM oven/bun:1-alpine

WORKDIR /app

# Copy package files and lockfile
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start in development mode
CMD ["bun", "run", "dev"]
