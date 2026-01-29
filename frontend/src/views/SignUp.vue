<script lang="ts" setup>
import { ref } from 'vue';

import CredentialsForm from '../components/CredentialsForm.vue';

const emit = defineEmits<{
  addTask: [newTask: string]
}>();

const newTask = ref("");
const error = ref("");


</script>


<template>
  <h1>Sign Up</h1> 

  <CredentialsForm :formType="'signup'" />

</template>