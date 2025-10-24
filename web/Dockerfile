# Production multi-stage Dockerfile for the Next.js (shadcn) frontend
FROM node:20-alpine AS builder
WORKDIR /app

# Install deps (when building from repo root we need to copy web/package*.json)
COPY web/package*.json ./
RUN npm ci --silent

# Copy app source (from repo root) and data needed at build time
# Ensure public exists so runner can copy it even if empty
RUN mkdir -p /app/public
COPY web .
# Copy dataset so Next.js prerender can access it at /data
COPY data /data

# Build the Next.js app
RUN npm run build

# Runtime image
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy built output and public assets
COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

# Install production deps only
RUN npm ci --production --silent

EXPOSE 3000
CMD ["npm", "run", "start"]
