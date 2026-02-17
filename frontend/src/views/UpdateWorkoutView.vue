<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useWorkoutStore } from '../stores/workoutStore';
import api from '../api';
import WorkoutForm from '../components/WorkoutForm.vue';
import { parseApiError } from '../utils';

const router = useRouter();
const store = useWorkoutStore();
const isSubmitting = ref(false);
const errorMessage = ref("");

const emit = defineEmits(['session-expired']);

const workoutToEdit = store.selectedWorkout;

// Redirect if lost (e.g. user refreshed on this page and store is empty)
if (!workoutToEdit) {
    router.push('/');
}

async function handleUpdateSubmit(payload: any) {
    isSubmitting.value = true;
    errorMessage.value = "";
    
    try {
        const token = sessionStorage.getItem('jwt');
        
        await api.post(`/user/update-workout/${workoutToEdit!.workout_name}`, payload, {
            headers: { Authorization: `Bearer ${token}` }
        });

        // Update the store with the new values so the View page is correct
        store.setWorkout(payload.workout);
        
        // Go back to the Details view
        router.push('/workout'); 

    } catch (error: any) {
        errorMessage.value = parseApiError(error, () => emit('session-expired'))
    } finally {
        isSubmitting.value = false;
    }
}
</script>


<template>
    <div v-if="workoutToEdit">
        <h1>Update Workout</h1>
        <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>

        <WorkoutForm 
            :initial-workout="workoutToEdit"
            :is-submitting="isSubmitting"
            submit-button-text="Update Workout"
            @submit="handleUpdateSubmit"
            @cancel="router.push('/')"
        />
    </div>
</template>