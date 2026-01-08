import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { HttpError } from '../utils/http-error.js';

export const errorHandler = (
  err: Error, 
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
    let statusCode = 500;
    let message = 'Internal Server Error';
    let details: any = undefined;

    if (err instanceof HttpError) {
        statusCode = err.statusCode;
        message = err.message;
    } else if (err instanceof z.ZodError) {
        statusCode = 400; // Bad Request
        message = 'Validation Error';
        // Map the Zod errors to a clean format
        details = err.issues.map(e => ({
            path: e.path.join('.'), 
            message: e.message   
        }));
    } else  {
        console.error(err); 
    }

    res.status(statusCode).json({ message, details });
};