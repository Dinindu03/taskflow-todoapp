FROM node:24-alpine AS build

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build:css

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/index.html /usr/share/nginx/html/index.html
COPY --from=build /frontend/dashboard.html /usr/share/nginx/html/dashboard.html
COPY --from=build /frontend/public/styles.css /usr/share/nginx/html/styles.css
COPY --from=build /frontend/src/js /usr/share/nginx/html/src/js

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --quiet --output-document=/dev/null http://127.0.0.1/ || exit 1
