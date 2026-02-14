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

import api from './api'; // Import the instance you just created
import Swal from 'sweetalert2';

async function deleteAccount() {
  // Confirm intention
  if (!confirm("Are you sure you want to delete your account? This cannot be undone.")) {
    return; // User clicked "Cancel"
  }

  // This creates a popup with a password field
  const { value: password } = await Swal.fire({ 
    title: 'Confirm your password to delete the account:',
    input: 'password',

    // --- Styling Options ---
    width: '40vw',       
    padding: '1em',             
    background: '#2c3e50',      // Dark Blue-Gray  
    color: '#ffffff',           // Change text color to white
    confirmButtonColor: '#d33', // Custom button color
    // -----------------------

    inputLabel: 'Password',
    inputPlaceholder: 'Enter your password',
    inputAttributes: {
      autocapitalize: 'off',
      autocorrect: 'off'
    },
    showCancelButton: true
  });

  if (!password) return; // User cancelled.

  try {
    const token = sessionStorage.getItem('jwt');

    await api.post('/auth/delete-account', 
      { password },
      {headers: { Authorization: `Bearer ${token}` }}
    );

    // On Success: Notify and Logout
    alert("Your account has been successfully deleted.");
    logOut();

  } catch (error: any) {
    console.error("Delete Account Error:", error);
 
    if (error.response) {
      // Server responded with a specific error message
      const error_message = JSON.stringify(error.response.data.detail, null, 2)
      alert(`Failed to delete: ${error_message || "Server Error"}`);
    } else {
      // Network error
      alert("Network error. Could not reach the server.");
    }
  }
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

      <div class="nav-right">
        <a 
          v-if="isUserLogged" 
          href="#" 
          @click.prevent="deleteAccount()" 
          class="delete-btn"
        >
          Delete Account
        </a>
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
    align-items: right;
  }
  
  .logout-btn:hover {
    text-decoration: underline;
  }

  .nav-right {
    grid-column: 3;
    justify-self: end; /* Pushes content to the far right */
  }
  
  .delete-btn {
      color: #871010;
      cursor: pointer;
  }
  /* To prevent the page content from hiding under the fixed nav */
  body {
    padding-top: 90px;
  }
</style>