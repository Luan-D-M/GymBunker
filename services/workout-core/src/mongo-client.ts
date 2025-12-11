import { connect } from 'mongoose';

export const connectToDatabase = async () => {
  try {
    await connect('mongodb://root:password@127.0.0.1:27017/workout-core?authSource=admin',);  
    console.log("✅ Database connected (Pool Ready)");
  } catch (err) {
    console.error("❌ DB Error:", err);
    process.exit(1); // Kill the server if DB fails to start
  }
};