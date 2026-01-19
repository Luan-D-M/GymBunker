import { connect, disconnect } from 'mongoose';
import { dbConfig } from './dependencies.js';

export const connectToDatabase = async () => {
  const mongoUri = `mongodb://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/${dbConfig.dbName}?authSource=${dbConfig.authSource}`;
  
  try {
    await connect(mongoUri);
    console.log("✅ Database connected (Pool Ready)");
  } catch (err) {
    console.error("❌ DB Error:", err);
    process.exit(1); 
  }
};

export const closeDatabase = async () => {
  try {
    // Closes the default mongoose connection
    await disconnect(); 
    console.log("✅ Database connection closed");
  } catch (err) {
    console.error("❌ Error closing database:", err);
  }
}