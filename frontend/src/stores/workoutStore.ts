import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Workout } from '../types';

export const useWorkoutStore = defineStore('workout', () => {
  const selectedWorkout = ref<Workout | null>(null);

  function setWorkout(workout: Workout) {
    selectedWorkout.value = workout;
  }

  return { selectedWorkout, setWorkout }; 
}, 
{ persist: { 
    storage: sessionStorage  
}});