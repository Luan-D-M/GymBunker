import { UserWorkoutsModel } from '../data/models/user-workouts-model.js'
import { Workout } from '../data/schemas/workout-schema.js'

// Editing Workouts and Exercises is done in the front end.


export const createUser = async (user_id: string) : Promise<void> => {
   const result = await UserWorkoutsModel.findOne({ user_id })
    if (result) {
        throw new Error(`User ${user_id} already exists`)
    }
    //create () instantiates and saves the document
    await UserWorkoutsModel.create(   
        {user_id,
        workouts: []}
    ) 
}

export const deleteUser = async (user_id: string) : Promise<boolean> => {
    const result = await UserWorkoutsModel.deleteOne({ user_id })

    return result.deletedCount === 1
}

export const addWorkout = async (user_id: string, workout: Workout)  => {
    const userWorkouts = await UserWorkoutsModel.findOne({ user_id })
    if (!userWorkouts) {
        throw new Error(`User workout not found for user ${user_id}`)
    }

    userWorkouts.workouts.push(workout)
    return await userWorkouts.save()
};

export const deleteWorkout = async (user_id: string, workout_name: string) => {
    const result = await UserWorkoutsModel.findOneAndUpdate(
        { user_id },
        { $pull: { workouts: { workout_name } } },
        { new: true }
    );

    if (!result) throw new Error(`User workout not found for user ${user_id}`);

    return result
}

export const updateWorkout = async (
    user_id: string,
    workout_name: string,
    new_workout: Workout
)  => {
    const userWorkouts = await UserWorkoutsModel.findOne({ user_id })
    if (!userWorkouts) {
        throw new Error(`User workout not found for user ${user_id}`)
    }

    const workout = userWorkouts.workouts.find(w => w.workout_name === workout_name);
    if (!workout) {
        throw new Error(`Workout '${workout_name}' not found`);
    }

    workout.set(new_workout);
    return await userWorkouts.save();
}
