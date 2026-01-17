import {Server, ServerCredentials} from '@grpc/grpc-js';

import { UserManagementServiceService } from '../proto/usermanagement/v1/user_management.js';

import { createUser, deleteUser } from './handler.js';

// ToDo: -Secure Connection
//       -Tests for gRPC.

export const startGrpc = () => {
   
    const server = new Server();
    server.addService(UserManagementServiceService, {createUser, deleteUser});
    
    server.bindAsync('0.0.0.0:4000', ServerCredentials.createInsecure(), () => {
        console.log('gRPC server is running on 0.0.0.0:4000');
    });
}