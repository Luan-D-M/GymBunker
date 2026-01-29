<script lang="ts" setup>

import { ref } from 'vue';
import type { AuthForm } from '../types';

const props = defineProps<{
  formType: AuthForm
}>();

const emit = defineEmits(['signup-success', 'login-success'])

const username = ref("");
const password = ref("");
const passwordConfirmed = ref("");

const warningMessage = ref("");


function formSubmitted() {
    /* ToDo: send request to backend */

    if (props.formType === 'signup') {

        if (password.value !== passwordConfirmed.value) {
            warningMessage.value = "Passwords not matching!";

            return;
        }

        // Clean warning messages
        warningMessage.value = "";
    } else { // formType === 'login'
        // Todo: request and handle response
        const jwt = "jwt-placeholder"
        emit('login-success', username.value, jwt)  // sends username and jwt too
    }

}
</script>


<template>
    <form @submit.prevent="formSubmitted">
        <label for="username">Username: <br />
        <input v-model.trim="username" type="text" id="username" name="username" required> <br />
        </label>  
        
        <label for="password">Password: <br />
        <input v-model.trim="password" type="text" id="password" name="password" required> <br />
        </label>  

        <label v-if="props.formType === 'signup'" for="confirm-password">Confirm password: <br />
        <input v-model.trim="passwordConfirmed" type="text" id="confirm-password" name="confirm" required> <br />
        </label>  

        <input type="submit" value="Submit">
    </form>

    <p v-if="warningMessage" class="warning">
        {{ warningMessage }}
    </p>


</template>

<style scoped>
.warning {
  color: red;
  font-weight: bold;
  margin-top: 1rem;
}
</style>