<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import WorkoutForm from '../components/WorkoutForm.vue';
import { parseApiError } from '../utils';

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
        errorMessage.value = parseApiError(error, () => emit('session-expired'))
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