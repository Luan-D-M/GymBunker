//import express from 'express';
import { connectToDatabase } from './mongo-client.js';

// ToDo:
//  1- API 



//const app = express();

const start = async () => {
  // 1. Open the connection pool
  await connectToDatabase(); 
  
  // 2. Start listening for requests
  /*
  app.listen(3000, () => {
    console.log('Server running on 3000');
});
  // Somehow the API will check if the user is authenticated.


*/ 
};

start();