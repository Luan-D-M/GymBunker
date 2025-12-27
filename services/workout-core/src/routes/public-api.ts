import { Router, Request, Response } from 'express';

import { Workout } from '../data/schemas/workout-schema.js'
import { getUserData, addWorkout, updateWorkout, deleteWorkout } from '../logic/workout-logic.js';

// ToDo: Middleware Wrapper, removing the try/catch block from the endpoints
// ToDo: API testing.
// ToDo: validate user jwt token

const router = Router();

router.get('/:userId', async (req: Request, res: Response) => {
    try {
        const { userId } = req.params;
        const userData = await getUserData(userId);
        if (!userData) {
            return res.status(404).json({ message: "User not found" });
        }

        return res.status(200).json(userData);

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Internal server error' })
    }
});

router.post('/:userId/add-workout', async (req: Request, res: Response) => {
    try {
        const { userId } = req.params;
        const workoutData: Workout = req.body.workout;

        const updatedUser = await addWorkout(userId, workoutData);
        if (!updatedUser) {
            return res.status(404).json({ message: "User not found" });
        }

        return res.status(201).json(updatedUser);

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Internal server error' });
    }
});

router.post('/:userId/update-workout/:workoutName', async (req: Request, res: Response) => {
    try {
        const { userId, workoutName } = req.params;
        const updateData: Workout = req.body.workout

        const result = await updateWorkout(userId, workoutName, updateData);
        if (!result) {
            return res.status(404).json({ message: "User or Workout not found" });
        }
        return res.status(200).json(result);

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Internal server error' });
    }
});

router.patch('/:userId/delete-workout/:workoutName', async (req: Request, res: Response) => {
    try {
        const { userId, workoutName } = req.params;

        const result = await deleteWorkout(userId, workoutName);
        if (!result) {
            return res.status(404).json({ message: "User or Workout not found" });
        }
        return res.status(200).json({ message: "Workout deleted successfully", data: result });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Internal server error' });
    }
});


export default router;