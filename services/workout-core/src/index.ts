import express from 'express';
import router  from './routes/public-api.js'
import { connectToDatabase } from './mongo-client.js';
import { jwtAuthenticatorFabric } from './middlewares/jwt-authenticator.js';
import { errorHandler } from './middlewares/errorHandler.js';
import { importSPKI } from 'jose/key/import';
import { readFile } from 'fs/promises';

// Relative to 'npm start' with cwd ./authenticator
// ToDO: put this in an .env file  --> It probably won't work right now.
const PRIVATE_KEY_PATH = '../keys/jwtRS256.key.pub'
const keyString: string = await readFile(PRIVATE_KEY_PATH, 'utf-8');
const publicKey = await importSPKI(keyString, 'RS256');

const app = express();
const port = 3000; // ToDo: configute it with .env file

const start = async () => {
  //  Open the connection pool
  await connectToDatabase(); // ToDo: at some point should be closed.

  app.use(express.json()); // Middleware to parse JSON bodies

  app.use(jwtAuthenticatorFabric(publicKey));
  // Any request starting with '/user' goes to the userRouter
  app.use('/user', router); 
  app.use(errorHandler);

  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
};

start();