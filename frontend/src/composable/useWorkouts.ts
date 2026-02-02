// src/composables/useWorkouts.ts
import api from '../api';
import { ref } from 'vue';
import type { Workout } from '../types';

// With this composable, Api calls can be reused.
export function useWorkouts() {
  const workouts = ref<Workout[]>([]);
  const isLoading = ref(false);
  const error = ref<any>(null);


  const getWorkoutsApi = async (token: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await api.get('/user/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Update the local state
      workouts.value = response.data.workouts;
      
    } catch (err: any) {
      console.error("GetWorkouts error:", err);
      error.value = err; // Save the error so the component can check it
    } finally {
      isLoading.value = false;
    }
  };

  /* Function is not being used. (Is it necessary?)
  const getWorkoutByName = async (workoutName: string, token: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      if (workouts.value.length === 0) {
        await getWorkoutsApi(token); // Get use workouts data if needed.
      }
      // Search for that specific workout locally
      const localMatch = workouts.value.find(w => w.workout_name === workoutName);
      if (!localMatch) {
          error.value = "Workout not found";
      }
      return localMatch;

    } catch (err: any) {
      error.value = err.message;
    } finally {
      isLoading.value = false; 
    }
  };
  */

  // WorkoutName is unique and works akin to an id at backend.
  const deleteWorkoutApi = async (workoutName: string, token: string) => {
    if (!confirm("Are you sure you want to delete this workout?")) return false;
    
    isLoading.value = true;
    error.value = null;

    try {
      await api.delete(`/user/delete-workout/${workoutName}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Update local state after successful request
      workouts.value = workouts.value.filter(w => w.workout_name !== workoutName);
      return true; 

    } catch (err: any) {
      console.error(err);
      error.value = err.message || "Failed to delete";
      return false;

    } finally {
      isLoading.value = false;
    }
  };


  return {
    workouts,
    isLoading,
    error,
    getWorkoutsApi,
    deleteWorkoutApi,
  };
}