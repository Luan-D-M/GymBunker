 import { ExerciseSchema } from './exercise-schema.js';  
 import { Schema, InferSchemaType } from 'mongoose';
 
 export const WorkoutSchema = new Schema({
    workout_name: { type: String, required: true, unique: true },
    exercises: {
      type: [ExerciseSchema],
      required: true,
      default: []
   }, 
 }, { _id: false });


// Creates a TypeScript type based on the Schema rules above
export type Workout = InferSchemaType<typeof WorkoutSchema>;