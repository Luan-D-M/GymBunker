<script setup lang="ts">
import { ref, onMounted } from 'vue';

const username = ref("");
const jwt = ref("");
const isUserLogged = ref(false);

onMounted(() => {
  const storedUser = sessionStorage.getItem('username');
  const storedToken = sessionStorage.getItem('jwt');

  if (storedToken && storedUser) {
    username.value = storedUser;
    jwt.value = storedToken;
    isUserLogged.value = true;
    
    // getWorkouts(jwt.value);
  }
});


</script>


<template>
  <h1>Home</h1> <!-- Will display workouts when logged in-->
                <!-- Here it will be possible to delete workouts -->
                <!-- User can select a workout to visualize it!-->
  <h2 v-if="isUserLogged"> Hello, you are logged in, {{ username }} </h2>


</template>