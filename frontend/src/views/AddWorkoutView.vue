<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { isAxiosError } from 'axios';
import api from '../api';
import WorkoutForm from '../components/WorkoutForm.vue';
import { getErrorMessagesZod } from '../utils';

const router = useRouter();
const isSubmitting = ref(false);
const errorMessage = ref("");

const emit = defineEmits(['session-expired']);

async function handleAddSubmit(payload: any) {
    isSubmitting.value = true;
    errorMessage.value = "";
    
    try {
        const token = sessionStorage.getItem('jwt');
        await api.post('/user/add-workout', payload, {
            headers: { Authorization: `Bearer ${token}` }
        });
        router.push('/');
    } catch (error) {
        if (isAxiosError(error)) {
            console.error("Axios Error:", error);

            if (error.response) {
                const responseData = error.response.data as any;

                // Check if it is a Zod Validation Error
                if (responseData.details) {
                    errorMessage.value = getErrorMessagesZod(error as any);
                } else {
                    const serverMessage = responseData.detail || JSON.stringify(responseData);
                    errorMessage.value = `Server Error (${error.response.status}): ${serverMessage}`;
                }

                // Unauthorized jwt!
                if (error.response.status === 401) {
                    emit('session-expired');
                }
            } else {
                // Network Error (Server down, Timeout, CORS)
                errorMessage.value = error.message;
            }
        } else {
            // Handle non-Axios errors
            console.error("Unexpected Error:", error);
            errorMessage.value = "An unexpected error occurred.";
        }
    } finally {
        isSubmitting.value = false;
    }
}
</script>

<template>
    <h1>Create New Workout</h1>
    <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>
    
    <WorkoutForm 
        :is-submitting="isSubmitting"
        submit-button-text="Create Workout"
        @submit="handleAddSubmit"
        @cancel="router.push('/')"
    />
</template>