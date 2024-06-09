FROM node:22-alpine3.20

WORKDIR /app

COPY . /app

RUN npm install

EXPOSE 5173

ENTRYPOINT [ "npm" ]
CMD [ "run", "dev", "--", "--host" ]