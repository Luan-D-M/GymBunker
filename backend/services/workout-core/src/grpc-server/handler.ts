import {
    ServerUnaryCall,
    sendUnaryData,
    status
} from '@grpc/grpc-js';

import {
    CreateUserRequest,
    CreateUserResponse,
    DeleteUserRequest,
    DeleteUserResponse
} from '../proto/usermanagement/v1/user_management.js';

import { createUser as createUserInDatabase ,
         deleteUser as deleteUserFromDatabase} from '../logic/workout-logic.js';
import { HttpError } from '../utils/http-error.js';

export const createUser = async (
    call: ServerUnaryCall<CreateUserRequest, CreateUserResponse>,
    callback: sendUnaryData<CreateUserResponse>
) => {
    try {
        const userId: string = call.request.id
        await createUserInDatabase(userId)
        
        const response: CreateUserResponse = {};
        
        return callback(null, response);
    } catch (e: any) {
        console.error("❌ CRITICAL gRPC ERROR:", e);
        if (e instanceof HttpError && e.statusCode === 409) {
            return callback({ code: status.ALREADY_EXISTS, details: e.message });
        }

        return callback(
            {
                code: status.INTERNAL,
                details: "Could not create user",
                message: e.message
            },
            null
        )
    }
};


export const deleteUser = async (
    call: ServerUnaryCall<DeleteUserRequest, DeleteUserResponse>,
    callback: sendUnaryData<DeleteUserResponse>
) => {
    try {
        const userId: string = call.request.id
        await deleteUserFromDatabase(userId)
        
        const response: DeleteUserResponse = {};
        
        return callback(null, response);
    } catch (e: any) {
        return callback(
            {
                code: status.INTERNAL, 
                details: "Could not delete user",
                message: e.message
            },
            null
        )
    }
};