<script lang="ts" setup>
import { ref } from 'vue';

import CredentialsForm from '../components/CredentialsForm.vue';


</script>


<template>
  <h1>Log In</h1>

  <CredentialsForm :formType="'login'" />

</template>