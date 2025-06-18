
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install --production

COPY . .

RUN npm run build

FROM alpine:latest

WORKDIR /app

COPY --from=build /app/build ./build

CMD ["sh", "-c", "cp -r /app/build/* /app/build/ 2>/dev/null || true; tail -f /dev/null"] 