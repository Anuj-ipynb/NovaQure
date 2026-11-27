# Stage 1: Build React 19 / Vite application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency specifications
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source and build with relative API baseURL
COPY frontend/ ./
ENV VITE_API_BASE_URL=""
RUN npm run build

# Stage 2: High-performance Nginx static server and reverse proxy
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
