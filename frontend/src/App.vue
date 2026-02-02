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

/**
 * Logs out the user by clearing session storage and resetting state.
 *
 * @param goToLoginView - (Optional) If true, redirects to '/login'. 
 * If false, redirects to '/' (Home). Defaults to false.
 */
function logOut(goToLoginView = false) {
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('jwt');

  isUserLogged.value = false;
  username.value = "";

  router.push( goToLoginView ? '/login' : '/'); 
}

function sessionExpired() {
  alert("Session expired. Please login again.");
  logOut(true);
}
</script>

<template>
  <header>
    <nav>  <!-- Navigation Bar -->
      <RouterLink to="/">
        <img 
          src="/Logo-NoBg.png"
          class="nav-logo"
          alt="GymBunker logo: a bunker beneath mountains."
        />
      </RouterLink>
      <div class="nav-content">
        <RouterLink to="/">Home</RouterLink> |
        <span v-if="isUserLogged">
          <RouterLink to="/add-workout">Add Workout</RouterLink>
          <!--<RouterLink to="/update-workout">Update Workout</RouterLink>-->
          <a href="#" @click.prevent="logOut()" class="logout-btn">Logout</a>
        </span>
        <span v-else>
          <RouterLink to="/signup">SignUp</RouterLink>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/about">About</RouterLink>
        </span>
      </div>
    </nav>
  </header>
  <!-- The :key bellow forces the page to reload when user log out. -->
  <RouterView :key="$route.fullPath + String(isUserLogged)"
              @login-success="onLoginSuccess"
              @session-expired="sessionExpired" 
  />
</template>

<style>
  nav {   
    position: fixed;
    top: 0;
    left: 0;
    width: 100%; 
    background-color: #333; 
    z-index: 1000;
    box-sizing: border-box;
    
    /* Using Grid to create 3 equal columns */
    display: grid;
    grid-template-columns: 1fr auto 1fr; 
    align-items: center;
    padding: 10px 20px;
    height: 90px; /* Force height to accommodate the 70px logo + padding */
  }

  .nav-logo {
    grid-column: 1; /* Keeps logo in the first column */
    height: 70px;
    width: auto;
    display: block;
  }

  .nav-content {
    grid-column: 2; /* Forces links to the exact middle column */
    display: flex;
    align-items: center;
    color: white;
    white-space: nowrap;
  }

  nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
  }

  .logout-btn {
    color: #ff6b6b;
    cursor: pointer;
  }

  .logout-btn:hover {
    text-decoration: underline;
  }

  /* To prevent the page content from hiding under the fixed nav */
  body {
    padding-top: 90px;
  }
</style>