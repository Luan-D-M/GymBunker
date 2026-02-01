<script lang="ts" setup>

import { ref } from 'vue';
import { type AxiosResponse } from 'axios';

import { getErrorMessagesPydantic } from '../utils';
import api from '../api';

import type { AuthForm } from '../types';

const props = defineProps<{
  formType: AuthForm
}>();

const emit = defineEmits(['signup-success', 'login-success'])

const username = ref("");
const password = ref("");
const passwordConfirmed = ref("");

const warningMessage = ref("");
const successMessage = ref("");

function cleanMessages() {
    warningMessage.value = "";
    successMessage.value = "";
}

async function formSignUpSubmitted() {
    cleanMessages()
    if (password.value !== passwordConfirmed.value) {
        warningMessage.value = "Passwords not matching!";
        
        return;
    }

    let response: AxiosResponse;
    try {
        const payload = {
            username: username.value,
            password: password.value
        }
        
        response = await api.post('/auth/signup', payload);
        successMessage.value =  response.data.message

        emit('signup-success')
    } catch (error: any) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {  // Pydantic validation error
            warningMessage.value = getErrorMessagesPydantic(error);
        } else {  // Simple error
            warningMessage.value = detail;
        }
    }
}

async function formLogInSubmitted() {
    cleanMessages()
    let response: AxiosResponse;
        try {
            const payload = {
                username: username.value,
                password: password.value
            }
            
            response = await api.post('/auth/login', payload);
            
            successMessage.value = response.data.message;
            emit('login-success', response.data.username, response.data.access_token)

        } catch (error: any) {
            warningMessage.value = error.response.data.detail;
        }
}





</script>


<template>
    <form v-if="props.formType === 'signup'" @submit.prevent="formSignUpSubmitted">
        <label for="username">Username: <br />
        <input v-model.trim="username" type="text" id="username" name="username" required> <br />
        </label>  
        
        <label for="password">Password: <br />
        <input v-model.trim="password" type="password" id="password" name="password" required> <br />
        </label>  

        <label for="confirm-password">Confirm password: <br />
        <input v-model.trim="passwordConfirmed" type="password" id="confirm-password" name="confirm" required> <br />
        </label>  

        <input type="submit" value="Submit">
    </form>    

    <form v-else @submit.prevent="formLogInSubmitted">
        <label for="username">Username: <br />
        <input v-model.trim="username" type="text" id="username" name="username" required> <br />
        </label>  
        
        <label for="password">Password: <br />
        <input v-model.trim="password" type="password" id="password" name="password" required> <br />
        </label>  

        <input type="submit" value="Submit">
    </form>

    <p v-if="warningMessage" class="warning message">
        {{ warningMessage }}
    </p>

    <p v-if="successMessage" class="success message">
        {{ successMessage }}
    </p>

</template>

<style scoped>
.message {
    font-weight: bold;
    margin-top: 1rem;
}
.warning {
    color: red;
    white-space: pre-wrap;   /* So /n of the warnings are rendered too */
}
.success {
    color: lightgreen;
}
</style>