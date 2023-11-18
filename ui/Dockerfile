FROM node:18-alpine
WORKDIR /app
COPY ./ui/package.json .
RUN yarn install
COPY ./ui .
CMD ["yarn", "start"]