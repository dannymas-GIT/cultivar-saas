# Production build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --legacy-peer-deps

COPY . .
ARG PUBLIC_API_URL=http://localhost:8000
ARG PUBLIC_ENV=staging
ENV PUBLIC_API_URL=$PUBLIC_API_URL
ENV PUBLIC_ENV=$PUBLIC_ENV
RUN npm run build

# Production serve
FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/static ./static
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev --legacy-peer-deps

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=80
EXPOSE 80

CMD ["node", "build"]
