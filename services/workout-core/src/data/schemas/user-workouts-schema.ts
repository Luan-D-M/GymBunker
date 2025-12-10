 import { WorkoutSchema } from './workout-schema.js';  
 import { Schema } from 'mongoose';
 
 export const UserWorkoutsSchema = new Schema({
    user_id: {
        type: String, required: true,
        unique: true,  // Also enforces indexing for this field
    },
    workouts:[WorkoutSchema],
 });