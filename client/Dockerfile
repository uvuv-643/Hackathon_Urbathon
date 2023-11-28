FROM node:16 as build-stage
WORKDIR /react
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM nginx as production-stage
EXPOSE 3000
RUN mkdir /react
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /react/build /react
