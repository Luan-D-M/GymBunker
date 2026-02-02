<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';

import { useWorkoutStore } from '../stores/workoutStore';
import { useWorkouts } from '../composable/useWorkouts';
import type { Workout } from '../types';

const username = ref("");
const jwt = ref("");
const isUserLogged = ref(false);

const router = useRouter()

const { setWorkout } = useWorkoutStore();

const { workouts, isLoading, error, 
        getWorkoutsApi, deleteWorkoutApi } = useWorkouts();


const emit = defineEmits(['session-expired']);

onMounted(async () => {
  const storedUser = sessionStorage.getItem('username');
  const storedToken = sessionStorage.getItem('jwt');

  if (storedToken && storedUser) {
    username.value = storedUser;
    jwt.value = storedToken;
    isUserLogged.value = true;
    
    await getWorkoutsApi(jwt.value)
    // Auto-logout if token is invalid (401)
    if (error.value && error.value.response && error.value.response.status === 401) {
        emit('session-expired');
    }
    
  }
});


function handleWorkoutView(workout: Workout) {
  setWorkout(workout)
  router.push('/workout')
}

async function handleWorkoutDelete(workoutName: string) {
  await deleteWorkoutApi(workoutName, jwt.value);
}

</script>


<template>
  <div v-if="isUserLogged"> 
    <h1> Hello, {{ username }}! </h1>  
    <h2> Your Workouts </h2>
    <hr />
  </div>
  <div v-else>
    <h3>
      Create an account to enjoy <strong>GymBunker!</strong>
    </h3> 
  </div>

  <div v-if="isLoading">
    <h2> Loading... </h2>
  </div>  

  <div v-else-if="workouts.length > 0">
    <ul>
      <li v-for="(workout) in workouts" :key="workout.workout_name" style="margin-bottom: 10px;">
        
        <strong>{{ workout.workout_name }}</strong> 
        ({{ workout.exercises.length }} exercises)

        <button @click="handleWorkoutView(workout)" style="margin-left: 10px;">View</button>
        <button @click="handleWorkoutDelete(workout.workout_name)" style="margin-left: 5px; color: red;">Delete</button>
        
      </li>
    </ul>
  </div>

  <div v-else-if="isUserLogged">
    <p>No workouts found. <RouterLink to="/add-workout">Add one?</RouterLink></p>
  </div>

  <!-- ToDo: Show error message
    <div v-if="error.value">
      <p> {{ error.value }}
      </div>
  -->

</template>