import { model } from 'mongoose';
import { UserWorkoutsSchema } from '../schemas/user-workouts-schema.js';

export const UserWorkoutsModel = model('UserWorkouts', UserWorkoutsSchema);