import { env } from 'node:process';

// Helper to ensure no variable is missing
const getEnvVar = (key: string): string => {
  // 1. debug: Print what Node actually sees!
  if (process.env[key] === undefined) {
    console.log(`⚠️  DEBUG: Could not find '${key}'. Available keys are:`);
    console.log(Object.keys(process.env).sort());
  }

  // 2. Access process.env directly (safer than destructuring in some setups)
  const value = process.env[key];

  if (!value) {
    console.error(`❌ WARNING: Missing required environment variable: ${key}`);
    process.exit(1);
  }
  return value;
};

export const dbConfig = {
  user: getEnvVar('MONGO_USER'),
  password: getEnvVar('MONGO_PASSWORD'),
  host: getEnvVar('MONGO_HOST'),
  port: getEnvVar('MONGO_PORT'),
  dbName: getEnvVar('MONGO_DB_NAME'),
  authSource: getEnvVar('MONGO_AUTH_DB'),
};