<script lang="ts" setup>
import CredentialsForm from '../components/CredentialsForm.vue';

const emit = defineEmits(['login-success'])

function onLoginSuccess(username: string, jwt: string) {
  emit('login-success', username, jwt)
}

</script>


<template>
  <h1>Log In</h1>

  <CredentialsForm :formType="'login'" @login-success="onLoginSuccess" />

</template>