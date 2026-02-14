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
    const clean_workout_name = workout.workout_name.trim()
    workout.workout_name = clean_workout_name

    const result = await UserWorkoutsModel.updateOne(
        { 
            user_id, 
            "workouts.workout_name": { $ne: clean_workout_name } 
        },
        { 
            $push: { workouts: workout } 
        }
    );

    if (result.modifiedCount === 0) {
        // If update failed, check if it was 404 (User missing) or 409 (Duplicate)
        const userExists = await UserWorkoutsModel.exists({ user_id });
        if (!userExists) {
            throw new HttpError(`User ${user_id} not found`, 404);
        } else {
            throw new HttpError(`Workout name '${clean_workout_name}' already exists.`, 409);
        }
    }

    return getUserData(user_id);
};

export const updateWorkout = async (
    user_id: string,
    workout_name: string,
    new_workout: WorkoutDTO
)  => {

    if (workout_name !== new_workout.workout_name) {
        throw new HttpError(
            `Workout name mismatch. The URL parameter '${workout_name}' does not match the
            body property '${new_workout.workout_name}'.`,
            400
        );
    }

    const clean_workout_name = workout_name.trim()

    const result = await UserWorkoutsModel.findOneAndUpdate(
        // Query
        { user_id,  
          "workouts.workout_name" : clean_workout_name
        },
        // Update
        {
            $set: { "workouts.$": new_workout }
        },
        // Options
        {
            new: true,
        }
    ) 

    if (!result) {
        // If null, it means either the User didn't exist OR the Workout didn't exist
        throw new HttpError(`User ${user_id} or Workout '${clean_workout_name}' not found`, 404);
    }

    return result;
}

export const deleteWorkout = async (user_id: string, workout_name: string) => {
    const clean_workout_name = workout_name.trim()
    const result = await UserWorkoutsModel.findOneAndUpdate(
        { user_id },
        { $pull: { workouts: { workout_name: clean_workout_name } } },
        { new: true }
    );
    
    if (!result) {
         throw new HttpError(`User workout not found for user ${user_id}`, 404);
    }
    
    return result
}

// Used by gRPC
export const createUser = async (user_id: string) : Promise<void> => {
    try{
        //create () instantiates and saves the document
        await UserWorkoutsModel.create(   
            {user_id,
            workouts: []}
        ) 
    } catch (error: any) {  // https://www.mongodb.com/docs/manual/reference/error-codes/
        if (error.code === 11000) { // code for DuplicateKey
           throw new HttpError(`User ${user_id} already exists`, 409);
       }
       throw error
    }
}

// Used by gRPC
export const deleteUser = async (user_id: string) : Promise<boolean> => {
    const result = await UserWorkoutsModel.deleteOne({ user_id })

    return result.deletedCount === 1
}