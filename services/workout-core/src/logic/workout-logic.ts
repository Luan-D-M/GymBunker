import { UserWorkoutsModel } from '../data/models/user-workouts-model.js'
import { Workout } from '../data/schemas/workout-schema.js'
import { UserWorkoutDTO, WorkoutDTO } from '../data/types/user-workout-dto.js';
import { HttpError } from '../utils/http-error.js';

// Editing Workouts and Exercises is done in the front end.

export const getUserData = async (user_id: string) : Promise<UserWorkoutDTO>  => {
    // lean() is faster: https://mongoosejs.com/docs/tutorials/lean.html
    const result = await UserWorkoutsModel.findOne({ user_id })
        .select('-_id -__v')  // Exclude internal MongoDB fields.
        .lean<UserWorkoutDTO>();
    
    if (!result) {
        throw new HttpError(`User ${user_id} not found`, 404);
    }

    return result;
}


export const addWorkout = async (user_id: string, workout: WorkoutDTO)  => {
    const userWorkouts = await UserWorkoutsModel.findOne({ user_id })
    if (!userWorkouts) {
        throw new HttpError(`User ${user_id} not found`, 404)
    }

    const isDuplicate = userWorkouts.workouts.some(
        (w) => w.workout_name.toLowerCase() === workout.workout_name.toLowerCase()
    );
    if (isDuplicate) {
        throw new HttpError(`Workout '${workout.workout_name}' already exists.`, 409)
    }

    userWorkouts.workouts.push(workout)
    return userWorkouts.save()
};

export const updateWorkout = async (
    user_id: string,
    workout_name: string,
    new_workout: WorkoutDTO
)  => {
    const userWorkouts = await UserWorkoutsModel.findOne({ user_id })
    if (!userWorkouts) {
        throw new HttpError(`User ${user_id} not found`, 404)
    }

    const workout = userWorkouts.workouts.find(w => w.workout_name === workout_name);
    if (!workout) {
        throw new HttpError(`Workout '${workout_name}' not found`, 404);
    }
    
    workout.set(new_workout);
    return userWorkouts.save();
}

export const deleteWorkout = async (user_id: string, workout_name: string) => {
    const result = await UserWorkoutsModel.findOneAndUpdate(
        { user_id },
        { $pull: { workouts: { workout_name } } },
        { new: true }
    );
    
    if (!result) {
         throw new HttpError(`User workout not found for user ${user_id}`, 404);
    }
    
    return result
}

// Used by gRPC
export const createUser = async (user_id: string) : Promise<void> => {
   const result = await UserWorkoutsModel.findOne({ user_id })
    if (result) {
        throw new HttpError(`User ${user_id} already exists`, 409)
    }
    //create () instantiates and saves the document
    await UserWorkoutsModel.create(   
        {user_id,
        workouts: []}
    ) 
}

// Used by gRPC
export const deleteUser = async (user_id: string) : Promise<boolean> => {
    const result = await UserWorkoutsModel.deleteOne({ user_id })

    return result.deletedCount === 1
}