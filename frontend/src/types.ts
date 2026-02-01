export type AuthForm = "signup" | "login"; 

// Auth service at backend uses Pydantic for validations
export type PydanticResponse = {
    detail: PydanticError[];
};
export type PydanticError = {  
  loc: (string | number)[];
  msg: string;
  type: string;
}

// Workout-core service at backend uses ZOD for validations
export type ZodResponse = {
    message: string;
    details: ZodErrorDetail[];
}
export type ZodErrorDetail =  {
    path: string;    
    message: string;
}


export type Workout = {
    workout_name: string;
    exercises: Exercise[];
}

export type Exercise = {
    name: string;
    weight?: number | null;
    number_sets?: number | null;
    number_reps?: number | null;
    rest_time_in_seconds?: number | null;
}


