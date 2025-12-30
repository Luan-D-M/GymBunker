import { HttpError } from "./http-error.js";

export class AuthenticationError extends HttpError {

  constructor(message: string) {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}