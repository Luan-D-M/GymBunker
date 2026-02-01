import type { AxiosError } from "axios";
import type { PydanticError, PydanticResponse, ZodResponse } from "./types";

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

        // 1. Smart Formatting: Convert "exercises.0.weight" -> "Exercise 1 - Weight"
        if (fieldName.includes('exercises.')) {
            fieldName = fieldName.replace(/exercises\.(\d+)\./, (_, index) => {
                return `Exercise ${Number(index) + 1} - `;
            });
        }

        // 2. Clean up common snake_case (e.g. "number_sets" -> "Number sets")
        fieldName = fieldName.replace(/_/g, ' ');

        // 3. Capitalize the result
        // (Assuming you have this helper, or just use inline logic)
        fieldName = capitalizeFirstLetter(fieldName); 

        return `${fieldName}: ${err.message}`;
    }).join('.\n');

    return errorMessage;
}