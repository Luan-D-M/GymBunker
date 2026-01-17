import { z } from 'zod';

export const ExerciseZodSchema = z.object({
    name: z.string().min(1, "Exercise name cannot be empty"),
    weight: z.number().min(0, "Weight cannot be negative").optional(), 
    number_sets: z.number().int().min(0, "Sets must be a positive integer").optional(),
    number_reps: z.number().int().min(0, "Reps must be a positive integer").optional(),
    rest_time_in_seconds: z.number().int().min(0).optional()
});