FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./
# npm ci is faster than npm install
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000
EXPOSE 4000 

#ENTRYPOINT ["npm", "start"]
# Mimics npm start to bypass signal propagation issues with npm
ENTRYPOINT ["node", "dist/src/index.js"]  