import { Request, Response, NextFunction } from "express";
import { jwtVerify } from "jose";
import { AuthenticationError } from "../utils/authentication-error.js";
import { JWSInvalid, JWSSignatureVerificationFailed, JWTExpired } from "jose/errors";

// ToDo: CryptoKey is the right type?
export const jwtAuthenticatorFabric = (publicKey: CryptoKey) => {
    return async (req: Request, res: Response, next: NextFunction) => {
        return jwtAuthenticator(publicKey, req, res, next);
    };
}

const jwtAuthenticator = async (publicKey: CryptoKey, req: Request, res: Response, next: NextFunction) => {
    try {
        const authHeader = req.headers.authorization;
        if (!authHeader) throw new AuthenticationError("No token provided");
        
        const token = authHeader.split(" ")[1]; // "Bearer ${jwtToken}"
        
        const { payload } = await jwtVerify(token, publicKey);

        res.locals.username = payload.username;   // https://expressjs.com/en/api.html#res.locals
        next(); 

    } catch (err: any) {
        // Catch the Jose error and turn it into a 401
        if (err instanceof JWSSignatureVerificationFailed) {
            return next(new AuthenticationError("Token verification failed"))
        } else if (err instanceof JWTExpired) { 
            return next(new AuthenticationError("Token was expired"))
        } else if  (err instanceof JWSInvalid) {
            return next(new AuthenticationError("Token is invalid (malformed)"))
        } else {
            return next(new AuthenticationError(err.message)); 
        }
    }
};