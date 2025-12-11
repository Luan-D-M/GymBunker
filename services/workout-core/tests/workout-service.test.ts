import mongoose, { Types } from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import { addWorkout, createUser, deleteUser, deleteWorkout, updateWorkout } from '../src/logic/workout-logic.js';
import { UserWorkoutsModel } from '../src/data/models/user-workouts-model.js';
import { Workout } from '../src/data/schemas/workout-schema.js';

// ToDo: Tests could be cleaner 

let mongoServer: MongoMemoryServer;

const getMockUserId = () => 'user-123';
const createUserWithoutWorkoutsInDatabase = async (): Promise<void> => {
  const initialData = new UserWorkoutsModel({
    user_id: getMockUserId(),
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
test('createUser: should add a user with no workouts to the database', async() => {
  await createUser(getMockUserId())

  const result = await UserWorkoutsModel.findOne({user_id : getMockUserId()})
  expect(result).toBeDefined()
  expect(result!.user_id).toEqual(getMockUserId())
  expect(result!.workouts).toEqual([])
})


test('createUser: should throw an error if the user already exists', async() => {
  await createUserWithoutWorkoutsInDatabase()
  await expect(createUser(getMockUserId()))
  .rejects
  .toThrow(`User ${getMockUserId()} already exists`)
})


test('deleteUser: should delete the user from database', async() => {
  await createUserWithoutWorkoutsInDatabase()
  const has_deleted_user = await deleteUser(getMockUserId())
  expect(has_deleted_user).toBe(true)

  const result = await UserWorkoutsModel.findOne({user_id : getMockUserId()})
  expect(result).toBeNull()
})


test('addWorkout: should add a workout to an existing user', async () => {
  await createUserWithoutWorkoutsInDatabase();

  const newWorkout: Workout = {
    workout_name: 'Leg Day',
    exercises: new Types.DocumentArray([])
  }; 
  const result = await addWorkout(getMockUserId(), newWorkout);

  expect(result).toBeDefined();
  expect(result.workouts).toHaveLength(1);
  expect(result.workouts[0].workout_name).toBe('Leg Day');

  const inDb = await UserWorkoutsModel.findOne({ user_id: getMockUserId() });
  expect(inDb?.workouts[0].workout_name).toBe('Leg Day');
});


test('addWorkout: should throw an error if user does not exist', async () => {
  const newWorkout: Workout =  { 
    workout_name: 'Chest Day',
    exercises: new Types.DocumentArray([]) 
  };

  await expect(addWorkout(getMockUserId(), newWorkout))
    .rejects
    .toThrow(`User workout not found for user ${getMockUserId()}`);
});


test('deleteWorkout: should remove a workout by name', async () => {
   await new UserWorkoutsModel({
    user_id: getMockUserId(),
    workouts: [{ workout_name: 'Cardio' }, { workout_name: 'Strength' }]
  }).save();

  const result = await deleteWorkout(getMockUserId(), 'Cardio');

  expect(result.workouts).toHaveLength(1);
  expect(result.workouts[0].workout_name).toBe('Strength');
});


test('updateWorkout: should update an existing workout', async () => {
  await new UserWorkoutsModel({
    user_id: getMockUserId(),
    workouts: [{ workout_name: 'Monday Routine', exercises: [] }]
  }).save();

  const updatedWorkout: Workout = { 
    workout_name: 'Monday Routine', 
    exercises: new Types.DocumentArray([{ name: 'Squats', number_sets: 3, number_reps: 10 }]) 
  };

  const result = await updateWorkout(getMockUserId(), 'Monday Routine', updatedWorkout);
  const specificWorkout = result.workouts.find(w => w.workout_name === 'Monday Routine');
  
  expect(specificWorkout).toBeDefined();
  expect(specificWorkout!.exercises[0].name).toBe('Squats');
});


test('updateWorkout: should throw error if workout name isnt found', async () => {
  await createUserWithoutWorkoutsInDatabase();
  const missingWorkout = 'Ghost Workout'
  const fakeUpdate = { workout_name: missingWorkout } as any;

  await expect(updateWorkout(getMockUserId(), missingWorkout, fakeUpdate))
    .rejects
    .toThrow(`Workout '${missingWorkout}' not found`);
});