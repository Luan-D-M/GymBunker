import { integerType } from './schema-utils.js';  // .js because not using a bundler
import { Schema } from 'mongoose';

export const ExerciseSchema = new Schema({
    name: { type: String, required: true },
    weight: Number, 
    number_sets: integerType,
    number_reps: integerType,
    rest_time_in_seconds: integerType,
}, { _id: false });