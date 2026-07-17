# ERIP Frontend 生产镜像：multi-stage Vite build + nginx SPA.
# 不 COPY .env；不暴露 Backend Secret。

FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY index.html ./
COPY tsconfig.json tsconfig.app.json tsconfig.node.json vite.config.ts ./
COPY src ./src

# 构建期仅公开配置；API 由 nginx 同源反代 /api
ENV VITE_APP_TITLE="Retail Insight AI"
RUN npm run build

FROM nginx:1.29-alpine

# 非特权探测依赖
RUN apk add --no-cache curl

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
  CMD curl -fsS http://127.0.0.1/ >/dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
