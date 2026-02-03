<script setup lang="ts">
import { ref, toRaw, onMounted } from 'vue';
import type { Exercise, Workout } from '../types';

const props = defineProps<{
  initialWorkout?: Workout | null; // Only present if editing
  isSubmitting: boolean;
  submitButtonText?: string;
}>();

const emit = defineEmits<{
  (e: 'submit', payload: any): void;
  (e: 'cancel'): void;
}>();

const workoutName = ref("");
// Initialize with one empty exercise so the form isn't blank
const exercises = ref<Exercise[]>([
    { name: "", weight: null, number_sets: null, number_reps: null, rest_time_in_seconds: null }
]);

// If Editing (Updating), load the data
onMounted(() => {
    if (props.initialWorkout) {
        workoutName.value = props.initialWorkout.workout_name;
        // Create a deep copy to break reactivity with the Store/Parent
        exercises.value = structuredClone(toRaw(props.initialWorkout.exercises));
    }
});

function addExercise() {
    exercises.value.push({
        name: "", weight: null, number_sets: null, number_reps: null, rest_time_in_seconds: null
    });
}

/**
* Remove the exercise.
* If it is the only exercise left, clean its info instead of removing it.
*/
function removeExercise(index: number) {
    if (exercises.value.length > 1) {
        exercises.value.splice(index, 1);
    } else {
        const first = exercises.value[0];
        if (first) {
            first.name = "";
            first.weight = null;
            first.number_sets = null; 
            first.number_reps = null;
            first.rest_time_in_seconds = null;
        }
    }
}

function sanitizeExercises(exercises: Exercise[]) {
    return exercises.map((exercise) => {
        // Creates a deep copy to avoid problems with Vue reactivity
        const clean = structuredClone(toRaw(exercise)); 
        Object.keys(clean).forEach((key) => {
            const k = key as keyof typeof clean;  // Tell TypeScript this string is a valid key of 'Exercise'
            if (clean[k] === null || clean[k] === "") {
                delete clean[k];
            }
        });
        return clean;
    });
}

function handleSubmit() {
    const workout: Workout = {
        workout_name: workoutName.value,
        exercises: sanitizeExercises(exercises.value)
    };
    
    emit('submit', { workout });
}
</script>

<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit">
        <div class="main-input">
            <label for="w-name">Workout Name:</label>
            <input 
                v-model.trim="workoutName" 
                type="text" 
                id="w-name" 
                placeholder="e.g. Leg Day" 
                required 
                :disabled="!!initialWorkout"  
                /> <!-- Disabled because workout name is its id at backend -->
            </div>

        <hr />   

        <h3>Exercises</h3>
        <div v-for="(exercise, index) in exercises" :key="index" class="exercise-card">
            <div class="header-row">
                <span>Exercise #{{ index + 1 }}</span>
                <button type="button" @click="removeExercise(index)" class="remove-btn">✕</button>
            </div>

            <div class="inputs-grid">
                <div class="full-width">
                    <input v-model.trim="exercise.name" placeholder="Exercise Name" required />
                </div>
                <input 
                    v-model.number="exercise.weight"
                    type="number"
                    min="0" 
                    step="any" 
                    placeholder="Weight (kg)" 
                />
                <input 
                    v-model.number="exercise.number_sets" 
                    type="number" 
                    min="0" 
                    placeholder="Sets" 
                />
                <input 
                    v-model.number="exercise.number_reps" 
                    type="number" 
                    min="0" 
                    placeholder="Reps" 
                />
                <input 
                    v-model.number="exercise.rest_time_in_seconds" 
                    type="number" 
                    min="0" 
                    placeholder="Rest (sec)" 
                />
            </div>
        </div>

        <button type="button" @click="addExercise" class="add-btn">+ Add Exercise</button>

        <div class="actions">
            <button type="submit" :disabled="isSubmitting" class="submit-btn">
                {{ isSubmitting ? 'Saving...' : (submitButtonText || 'Save') }}
            </button>
            <button type="button" @click="$emit('cancel')" class="cancel-btn">Cancel</button>
        </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 600px; /* Wider to fit inputs */
  margin: 0 auto;
}

.main-input {
    margin-bottom: 2rem;
}
.main-input input {
    width: 100%;
    padding: 0.8rem;
    font-size: 1.2rem;
}

/* Exercise Card Style */
.exercise-card {
    background: #fdfdfd;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.header-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
}

.inputs-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* 2 columns */
    gap: 10px;
}

.full-width {
    grid-column: 1 / -1; /* Span both columns */   /* grid-column: start-line / end-line */
}

input {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
}

/* Buttons */
.add-btn {
    width: 100%;
    padding: 0.8rem;
    background-color: #f0f0f0;
    border: 2px dashed #ccc;
    color: #555;
    cursor: pointer;
    margin-bottom: 2rem;
}
.add-btn:hover {
    background-color: #e9e9e9;
    border-color: #999;
}

.remove-btn {
    background: none; /* So theres only the red 'x' */
    border: none;
    color: red;
    font-size: 1.2rem;
    cursor: pointer;
}

.actions {
    display: flex;
    gap: 15px;
}
.submit-btn {
    background-color: #4CAF50;
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
}
.cancel-btn {
    background: none;
    border: 1px solid #ccc;
    padding: 1rem 2rem;
    border-radius: 4px;
    cursor: pointer;
}
</style>