import { jwtVerify } from "jose";

// ToDo: Improve this file.
// ToDo: Middleware to handle auth and errors. Dependencies files getting variables from env.

const verifyJwt = async (jwt: string, publicKey: CryptoKey, algorithm: string = "RS256") => {
    const { payload, protectedHeader } = await jwtVerify(jwt, publicKey, {algorithms: [algorithm]});

    return payload
}