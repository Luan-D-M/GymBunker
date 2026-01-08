import { Router, Request, Response } from 'express';

import { Workout } from '../data/schemas/workout-schema.js'
import { getUserData, addWorkout, updateWorkout, deleteWorkout } from '../logic/workout-logic.js';
import { HttpError } from '../utils/http-error.js';
import { WorkoutZodSchema } from '../data/schemas/workout-zod-schema.js';

// ToDo: API testing.
/*
* Starting with Express 5, route handlers and middleware that return a Promise will call next(value)
* automatically when they reject or throw an error.
* https://expressjs.com/en/guide/error-handling.html
*/

const router = Router();

/*
* User validation is done by the authenticator service.
* Here it isnt needed because the jwt is verified before any of this endpoints runs.
*/
router.get('/', async (req: Request, res: Response) => {
    const userId = res.locals.username;
    const userData = await getUserData(userId);
    
    return res.status(200).json(userData);
});

router.post('/add-workout', async (req: Request, res: Response) => {
    const userId = res.locals.username;
    const workoutData: Workout = req.body.workout;

    const validData = WorkoutZodSchema.parse(workoutData);
    const updatedUser = await addWorkout(userId, validData);
    if (!updatedUser) {
        throw new HttpError("User not found", 404);
    }

    return res.status(201).json(updatedUser);
});

router.post('/update-workout/:workoutName', async (req: Request, res: Response) => {
    const userId = res.locals.username;
    const { workoutName } = req.params;
    const updatedData: Workout = req.body.workout

    const validData = WorkoutZodSchema.parse(updatedData);
    const result = await updateWorkout(userId, workoutName, validData);

    return res.status(200).json(result);
});

router.delete('/delete-workout/:workoutName', async (req: Request, res: Response) => {
    const userId = res.locals.username;
    const { workoutName } = req.params;

    const result = await deleteWorkout(userId, workoutName);

    return res.status(200).json({ message: "Workout deleted successfully", data: result });
});


export default router;