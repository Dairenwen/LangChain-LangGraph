FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_API_BASE_URL=http://127.0.0.1:50699
ARG VITE_ASSISTANT_ID=agent
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_ASSISTANT_ID=$VITE_ASSISTANT_ID
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
