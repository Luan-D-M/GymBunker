import express from 'express';
import path from 'path';
import swaggerUi from 'swagger-ui-express';
import YAML from 'yamljs';
import { importSPKI } from 'jose/key/import';
import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';

import router  from './routes/public-api.js'
import { startGrpc } from './grpc-server/index.js';
import { connectToDatabase } from './mongo-client.js';
import { jwtAuthenticatorFabric } from './middlewares/jwt-authenticator.js';
import { errorHandler } from './middlewares/errorHandler.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const swaggerDocument = YAML.load(path.join(__dirname, './docs/openapi.yaml'));

const app = express();
const port = 3000; // ToDo: configute it with .env file

const start = async () => {
  try {
    //  Open the connection pool
    await connectToDatabase(); // ToDo: at some point should be closed.
    
    startGrpc()

    console.log('Reading private key...')

    // path.resolve(__dirname, '../../keys/jwtRS256.key.pub');
    const PRIVATE_KEY_PATH = path.resolve(
      __dirname,
      '../../../../keys/jwtRS256.key.pub'
    );
 
    const keyString: string = await readFile(PRIVATE_KEY_PATH, 'utf-8');
    const publicKey = await importSPKI(keyString, 'RS256');

    app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
    app.use(express.json()); // Middleware to parse JSON bodies

    app.use(jwtAuthenticatorFabric(publicKey));
    // Any request starting with '/user' goes to the userRouter
    app.use('/user', router); 
    app.use(errorHandler);

    app.listen(port, () => {
      console.log(`Server running on port ${port}`);
    });
  
  } catch (err) { 
    console.error("❌ CRITICAL STARTUP ERROR:", err);
    process.exit(1);
  }
};

start();