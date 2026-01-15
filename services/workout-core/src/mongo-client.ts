import { connect } from 'mongoose';
import { dbConfig } from './dependencies.js';

export const connectToDatabase = async () => {
  // Construct the URI dynamically using the config values
  const mongoUri = `mongodb://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/${dbConfig.dbName}?authSource=${dbConfig.authSource}`;

  try {
    // Log the connection attempt (masking the password for security)
    console.log(`🔌 Connecting to: mongodb://${dbConfig.user}:*****@${dbConfig.host}:${dbConfig.port}/${dbConfig.dbName}`);

    await connect(mongoUri);
    console.log("✅ Database connected (Pool Ready)");
  } catch (err) {
    console.error("❌ DB Error:", err);
    process.exit(1); // Kill the server if DB fails to start
  }
};