FROM node:20-slim

WORKDIR /app

# MongoMemoryServer needs libcurl4
RUN apt-get update && apt-get install -y libcurl4 && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json ./
# npm ci is faster than npm install
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000
EXPOSE 4000 

#CMD ["npm", "start"]
# Mimics npm start to bypass signal propagation issues with npm
CMD ["node", "dist/src/index.js"]  