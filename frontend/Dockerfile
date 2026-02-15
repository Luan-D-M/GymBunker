FROM node:20-slim

WORKDIR /app

COPY package.json package-lock.json ./
# npm ci is faster than npm install
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]

