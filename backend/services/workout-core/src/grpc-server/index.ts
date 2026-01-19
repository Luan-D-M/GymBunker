import {Server, ServerCredentials} from '@grpc/grpc-js';

import { UserManagementServiceService } from '../proto/usermanagement/v1/user_management.js';

import { createUser, deleteUser } from './handler.js';
import { serve } from 'swagger-ui-express';

// ToDo: -Secure Connection
//       -Tests for gRPC.
let server: Server

export const startGrpc = () => {
   
    server = new Server();
    server.addService(UserManagementServiceService, {createUser, deleteUser});
    
    server.bindAsync('0.0.0.0:4000', ServerCredentials.createInsecure(), () => {
        console.log('gRPC server is running on 0.0.0.0:4000');
    });
}

export const stopGrpc = () => {
    return new Promise<void>((resolve, reject) => {
        if (!server) return resolve();

        let shutdownComplete = false;
        const timeout_value_in_ms = 5000

        // Timeout to force shutdown
        const forceShutdownTimer = setTimeout(() => {
            if (!shutdownComplete) {
                console.warn("⚠️ gRPC shutdown timed out. Forcing shutdown...");
                server.forceShutdown(); 
                resolve();
            }
        }, timeout_value_in_ms);

        // Try to shut down gracefully
        server.tryShutdown((err) => {
            shutdownComplete = true;
            clearTimeout(forceShutdownTimer); // Cancel the kill switch
            
            if (err) {
                console.error("gRPC tryShutdown error, forcing...", err);
                server.forceShutdown();
            } else {
                console.log("✅ gRPC server closed gracefully.");
            }
            resolve();
        });
    });
};