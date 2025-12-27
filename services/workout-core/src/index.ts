import express from 'express';
import { connectToDatabase } from './mongo-client.js';
import router  from './routes/public-api.js'

// ToDo:
//  1- API



const app = express();
const port = 3000; // ToDo: configute it with .env file

const start = async () => {
  // 1. Open the connection pool
  await connectToDatabase(); // ToDo: at some point should be closed.

  app.use(express.json()); // Middleware to parse JSON bodies

  // MOUNT THE ROUTER
  // Any request starting with '/users' goes to the userRouter
  app.use('/users', router); 

  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
};

start();