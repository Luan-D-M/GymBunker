<script setup lang="ts">
import { ref, onMounted } from 'vue';

import api from '../api';

import type { Workout } from '../types';

const username = ref("");
const jwt = ref("");
const isUserLogged = ref(false);
const workouts = ref<Workout[]>([]);

const emit = defineEmits(['session-expired']);

onMounted(async () => {
  const storedUser = sessionStorage.getItem('username');
  const storedToken = sessionStorage.getItem('jwt');

  if (storedToken && storedUser) {
    username.value = storedUser;
    jwt.value = storedToken;
    isUserLogged.value = true;
    
    try {

      const response = await api.get('/user/', {
              headers: {
                  Authorization: `Bearer ${jwt.value}`
              }
          });
      workouts.value = response.data.workouts

    } catch (error: any) {
        console.error("Failed to fetch workouts:", error);

        // Auto-logout if token is invalid (401)
        if (error.response && error.response.status === 401) {
            emit('session-expired');
        }
    }
  }
});

</script>


<template>
  <h1>Home</h1>
  <h2 v-if="isUserLogged"> Hello, {{ username }}! </h2>

  <div v-if="workouts.length > 0">
    
    <ul>
      <li v-for="(workout, index) in workouts" :key="index" style="margin-bottom: 10px;">
        
        <strong>{{ workout.workout_name }}</strong> 
        ({{ workout.exercises.length }} exercises)

        <button style="margin-left: 10px;">View</button>
        <button style="margin-left: 5px; color: red;">Delete</button>
        
      </li>
    </ul>

  </div>

  <div v-else-if="isUserLogged">
    <p>No workouts found. <RouterLink to="/add-workout">Add one?</RouterLink></p>
  </div>

</template>