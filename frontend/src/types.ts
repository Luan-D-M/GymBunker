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