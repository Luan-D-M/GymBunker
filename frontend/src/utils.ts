import type { AxiosError } from "axios";
import type { PydanticError, PydanticResponse } from "./types";

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