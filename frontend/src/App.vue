<script setup lang = "ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink> |
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/signup">SignUp</RouterLink>
      <RouterLink to="/login">Login</RouterLink>
    </nav>
  </header>


  <RouterView />
</template>

<style>
  nav {   /* ToDo: Improve navbar */
      position: fixed; /* Fixes the element to the viewport */
      top: 0;
      left: 0;
      width: 100%; 
      background-color: #333; 
      padding: 1rem;
      z-index: 1000;
    }

  nav a {
    color: white;
    text-decoration: none;
    margin-right: 15px;
  }


</style>