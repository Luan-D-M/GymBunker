import mongoose, { Types } from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import { addWorkout, createUser, deleteUser,
        deleteWorkout, updateWorkout, getUserData } from '../src/logic/workout-logic.js';
import { UserWorkoutsModel } from '../src/data/models/user-workouts-model.js';
import { Workout } from '../src/data/schemas/workout-schema.js';
import { UserWorkoutDTO } from '../src/data/types/user-workout-dto.js';

// ToDo: Tests could be cleaner 

let mongoServer: MongoMemoryServer;

const MOCK_USER_ID = 'user-123';
const MOCK_WORKOUT = {
  workout_name: 'Chest Day',
  exercises: [
    {
      name: 'Bench Press',
      weight: 100,
      number_sets: 3,
      number_reps: 10,
      rest_time_in_seconds: 60
    },
    {
      name: 'Push Ups',
      weight: 0, // Bodyweight
      number_sets: 3,
      number_reps: 15
    }
  ]
};

const createUserWithoutWorkoutsInDatabase = async (): Promise<void> => {
  const initialData = new UserWorkoutsModel({
    user_id: MOCK_USER_ID,
    workouts: []
  });
  await initialData.save();
}

// Setup
beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();
  // Connects to the default mongoose instance (Singleton)
  await mongoose.connect(uri);
});

afterEach(async () => {
  // Clear the collection after every test to ensure isolation
  await UserWorkoutsModel.deleteMany({});
});

// Teardown
afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});


// Test Suites
describe('getUserData', () => {
  test('retrieves user data even when the user has no workouts', async () => {
    await createUserWithoutWorkoutsInDatabase()

    const expectedData: UserWorkoutDTO = {
      user_id: MOCK_USER_ID,
      workouts: []
    }
    const userData = await getUserData(MOCK_USER_ID)
    expect(userData).toEqual(expectedData)
  });

  test('returns error if the user is not found', async () => {
    await expect(getUserData(MOCK_USER_ID))
      .rejects
      .toThrow(`User ${MOCK_USER_ID} not found`)
  });

  test('returns the complete nested workout structure for an existing user', async () => {
    const expectedData: UserWorkoutDTO = {
      user_id: MOCK_USER_ID,
      workouts: [MOCK_WORKOUT]
    }
    // Insert mock data to database
    await UserWorkoutsModel.create({
      user_id: MOCK_USER_ID,
      workouts: [MOCK_WORKOUT]
    });

    const result = await getUserData(MOCK_USER_ID);

    expect(result).toEqual(expectedData)
  });
});


describe('createUser', () => {
  test('should add a user with no workouts to the database', async() => {
    await createUser(MOCK_USER_ID)

    const result = await UserWorkoutsModel.findOne({user_id : MOCK_USER_ID})
    expect(result).toBeDefined()
    expect(result!.user_id).toEqual(MOCK_USER_ID)
    expect(result!.workouts).toEqual([])
  });


  test('should throw an error if the user already exists', async() => {
    await createUserWithoutWorkoutsInDatabase()
    await expect(createUser(MOCK_USER_ID))
    .rejects
    .toThrow(`User ${MOCK_USER_ID} already exists`)
  });
});


describe('deleteUser', () => {
  test('removes the user from the database and returns true', async() => {
    await createUserWithoutWorkoutsInDatabase()
    const has_deleted_user = await deleteUser(MOCK_USER_ID)
    expect(has_deleted_user).toBe(true)

    const result = await UserWorkoutsModel.findOne({user_id : MOCK_USER_ID})
    expect(result).toBeNull()
  });

  test('doesnt find user in database and returns false', async() => {
    const has_deleted_user = await deleteUser(MOCK_USER_ID)
    expect(has_deleted_user).toBe(false)
  });
});


describe('addWorkout', () => {
  test('appends a new workout to an existing user', async () => {
    await createUserWithoutWorkoutsInDatabase();

    const newWorkout: Workout = {
      workout_name: 'Leg Day',
      exercises: new Types.DocumentArray([])
    }; 
    const result = await addWorkout(MOCK_USER_ID, newWorkout);

    expect(result).toBeDefined();
    expect(result.workouts).toHaveLength(1);
    expect(result.workouts[0].workout_name).toBe('Leg Day');

    const inDb = await UserWorkoutsModel.findOne({ user_id: MOCK_USER_ID });
    expect(inDb?.workouts[0].workout_name).toBe('Leg Day');
  });

  test('throws an error when the target user does not exist', async () => {
    const newWorkout: Workout =  { 
      workout_name: 'Chest Day',
      exercises: new Types.DocumentArray([]) 
    };

    await expect(addWorkout(MOCK_USER_ID, newWorkout))
      .rejects
      .toThrow(`User ${MOCK_USER_ID} not found`);
  });
});


describe('deleteWorkout', () => {
  test('removes the workout matching the provided name', async () => {
    await new UserWorkoutsModel({
      user_id: MOCK_USER_ID,
      workouts: [{ workout_name: 'Cardio' }, { workout_name: 'Strength' }]
    }).save();

    const result = await deleteWorkout(MOCK_USER_ID, 'Cardio');

    expect(result.workouts).toHaveLength(1);
    expect(result.workouts[0].workout_name).toBe('Strength');
  });
});


describe('updateWorkout', () => {
  test('updates an existing workout with the new workout data', async () => {
    await new UserWorkoutsModel({
      user_id: MOCK_USER_ID,
      workouts: [{ workout_name: 'Monday Routine', exercises: [] }]
    }).save();

    const updatedWorkout: Workout = { 
      workout_name: 'Monday Routine', 
      exercises: new Types.DocumentArray([{ name: 'Squats', number_sets: 3, number_reps: 10 }]) 
    };

    const result = await updateWorkout(MOCK_USER_ID, 'Monday Routine', updatedWorkout);
    const specificWorkout = result.workouts.find(w => w.workout_name === 'Monday Routine');
    
    expect(specificWorkout).toBeDefined();
    expect(specificWorkout!.exercises[0].name).toBe('Squats');
  });

  test('throws an error when the workout name does not exist for the user', async () => {
    await createUserWithoutWorkoutsInDatabase();
    const missingWorkout = 'Ghost Workout'
    const fakeUpdate = { workout_name: missingWorkout } as any;

    await expect(updateWorkout(MOCK_USER_ID, missingWorkout, fakeUpdate))
      .rejects
      .toThrow(`Workout '${missingWorkout}' not found`);
  });
});