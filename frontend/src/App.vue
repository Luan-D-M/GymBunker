<script setup lang = "ts">
import { ref, onMounted } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router'

const router = useRouter()

const isUserLogged = ref(false)
const username = ref("")

// So, if user refreshes the page, he continues logged on!
onMounted(() => {
  const token = sessionStorage.getItem('jwt');
  const savedUser = sessionStorage.getItem('username');

  if (token && savedUser) {
    isUserLogged.value = true;
    username.value = savedUser;
  }
});

function onLoginSuccess(usernameArg: string, jwt: string) {
  sessionStorage.setItem('username', usernameArg)
  sessionStorage.setItem('jwt', jwt)

  isUserLogged.value = true 
  username.value = usernameArg

  router.push('/')
}

function logOut() {
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('jwt');

  isUserLogged.value = false;
  username.value = "";

  router.push('/'); 
}


</script>

<template>
  <header>
    <nav>  <!-- Navigation Bar -->
      <RouterLink to="/">Home</RouterLink> |
      <span v-if="isUserLogged">
        <RouterLink to="/add-workout">Add Workout</RouterLink>
        <RouterLink to="/update-workout">Update Workout</RouterLink>
        <a href="#" @click.prevent="logOut" class="logout-btn">Logout</a>
      </span>
      <span v-else>
        <RouterLink to="/signup">SignUp</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </span>
    </nav>
  </header>

  <RouterView @login-success="onLoginSuccess" />
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

  .logout-btn {
    color: #ff6b6b; /* Light red to indicate 'exit' */
    margin-left: 15px;
    cursor: pointer;
    text-decoration: none;
  }

  .logout-btn:hover {
    text-decoration: underline;
  }

</style>