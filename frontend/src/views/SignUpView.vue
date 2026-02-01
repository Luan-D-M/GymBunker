<script lang="ts" setup>
import { useRouter } from 'vue-router';

import CredentialsForm from '../components/CredentialsForm.vue';

const router = useRouter();

function onSignUpSuccess() {
 // Wait 2s, so the user can read that account was created then redirect to login page.
 setTimeout(() => {
    router.push('/login');
  }, 2000);
}

</script>


<template>
  <h1>Sign Up</h1> 

  <CredentialsForm :formType="'signup'" @signup-success="onSignUpSuccess" />

</template>