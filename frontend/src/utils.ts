import type { AxiosError } from "axios";
import type { PydanticError, PydanticResponse, ZodResponse } from "./types";

import { isAxiosError } from 'axios';

export function capitalizeFirstLetter(val: string): string {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

export function getErrorMessagesPydantic(error: AxiosError<PydanticResponse>): string {
    // Extract the array 
    const details = error.response?.data.detail as PydanticError[];
    if (!details) return "Unknown validation error.";

    // Join all Pydantic errors
    const errorMessage = details.map((err) => {
        const fieldName = err.loc[err.loc.length - 1] as string;  // Get the field name (last item in the 'loc' array)
        return `${capitalizeFirstLetter(fieldName)}: ${err.msg}`;
    }).join('.\n') + '.';

    return errorMessage;
}

export function getErrorMessagesZod(error: AxiosError<ZodResponse>): string {
    // Extract the array
    const details = error.response?.data.details;
    if (!details) return "Unknown validation error.";

    // Join all Zod errors
    const errorMessage = details.map((err) => {
        let fieldName = err.path;

        // Convert "exercises.0.weight" -> "Exercise 1 - Weight"
        if (fieldName.includes('exercises.')) {
            fieldName = fieldName.replace(/exercises\.(\d+)\./, (_, index) => {
                return `Exercise ${Number(index) + 1} - `;
            });
        }

        // Clean up common snake_case (e.g. "number_sets" -> "Number sets")
        fieldName = fieldName.replace(/_/g, ' ');

        // Capitalize the result
        fieldName = capitalizeFirstLetter(fieldName); 

        return `${fieldName}: ${err.message}`;
    }).join('.\n');

    return errorMessage;
}


export function parseApiError(error: any, emitSessionExpired: () => void): string {

    if (isAxiosError(error)) {
        let errorMessage = "";
        console.error("Axios Error:", error);

        if (error.response) {
            const responseData = error.response.data as any;

            // Check if it is a Zod Validation Error
            if (responseData.details) {
                errorMessage = getErrorMessagesZod(error as any);
            } else {
                const serverMessage = responseData.detail || JSON.stringify(responseData);
                errorMessage = `Server Error (${error.response.status}): ${serverMessage}`;
            }
            // Unauthorized jwt!
            if (error.response.status === 401) {
                emitSessionExpired();
            }
        } else {
            // Network Error (Server down, Timeout, CORS)
            errorMessage = error.message;
        }

        return errorMessage
    }

    //  Non-Axios Error
    console.error("Unexpected Error:", error);
    return "An unexpected error occurred.";
}
    
