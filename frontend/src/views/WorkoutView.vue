<script setup lang="ts">
import { useWorkoutStore } from '../stores/workoutStore';
import { useRouter } from 'vue-router';

const workout = useWorkoutStore().selectedWorkout;
const router = useRouter();

function goBack() {
  router.push('/');
}
</script>

<template>
  <div class="workout-container" v-if="workout">
    <header class="workout-header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h1>{{ workout.workout_name }}</h1>
      <span class="exercise-count">{{ workout.exercises.length }} Exercises</span>
    </header>

    <div class="exercises-grid">
      <div 
        v-for="(exercise, index) in workout.exercises" 
        :key="index" 
        class="exercise-card"
      >
        <div class="card-header">
          <span class="index">#{{ index + 1 }}</span>
          <h3>{{ exercise.name }}</h3>
        </div>

        <div class="card-stats">
          <div class="stat" v-if="exercise.weight">
            <span class="label">Weight</span>
            <span class="value">{{ exercise.weight }} kg</span>
          </div>

          <div class="stat" v-if="exercise.number_sets">
            <span class="label">Sets</span>
            <span class="value">{{ exercise.number_sets }}</span>
          </div>

          <div class="stat" v-if="exercise.number_reps">
            <span class="label">Reps</span>
            <span class="value">{{ exercise.number_reps }}</span>
          </div>

          <div class="stat" v-if="exercise.rest_time_in_seconds">
            <span class="label">Rest</span>
            <span class="value">{{ exercise.rest_time_in_seconds }}s</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="empty-state">
    <p>No workout selected.</p>
    <button @click="goBack">Return Home</button>
  </div>
</template>

<style scoped>
.workout-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

/* Header */
.workout-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 2rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 1rem;
}

.workout-header h1 {
  margin: 0.5rem 0;
  font-size: 2.5rem;
  color: #7797b8;
}

.exercise-count {
  color: #666;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.back-btn {
  background: none;
  border: none;
  color: #566f89;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  margin-bottom: 0.5rem;
}

.back-btn:hover {
  text-decoration: underline;
}

/* Grid Layout */
.exercises-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Exercise Card */
.exercise-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.exercise-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.index {
  background-color: #f0f2f5;
  color: #888;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

/* Stats Grid inside Card */
.card-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
}

.value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

/* Empty State */
.empty-state {
  text-align: center;
  margin-top: 4rem;
  color: #666;
}
</style>