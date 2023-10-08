FROM node:latest


WORKDIR /frontend

COPY . .

RUN npm i
ENV PATH /frontend/node_modules/.bin:$PATH

EXPOSE 3000

CMD ["npm", "start"]



