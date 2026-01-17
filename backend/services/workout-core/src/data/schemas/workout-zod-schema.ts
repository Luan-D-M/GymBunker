import { z } from 'zod'; 
import { ExerciseZodSchema } from './exercise-zod-schema.js';

export const WorkoutZodSchema = z.object({
    workout_name: z.string().min(1, "Workout name is required"),
    exercises: z.array(ExerciseZodSchema).default([])
});
