export interface ExerciseDTO {
    name: string;
    weight?: number | null;
    number_sets?: number | null;
    number_reps?: number | null;
    rest_time_in_seconds?: number | null;
}

export interface WorkoutDTO {
    workout_name: string;
    exercises?: ExerciseDTO[] | null;
}

export interface UserWorkoutDTO {
    user_id: string;
    workouts: WorkoutDTO[];
}