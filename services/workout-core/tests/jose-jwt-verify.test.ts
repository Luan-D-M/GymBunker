import { importSPKI, jwtVerify, importPKCS8, SignJWT } from "jose";
import { JWSInvalid, JWSSignatureVerificationFailed, JWTExpired } from "jose/errors";


const ALGORITHM = 'RS256'

const createJWt = async (createExpiredJwt = false) => {
  const pkcs8 =  `-----BEGIN PRIVATE KEY-----
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
MjEW0GZNM1rEA3OkNRnyz0ZcGTXqeg==
-----END PRIVATE KEY-----`
  const privateKey = await importPKCS8(pkcs8, ALGORITHM)

  const expirationTime = createExpiredJwt ? '-1min' : '1min';
  const jwt = await new SignJWT({ 'urn:example:claim': true })
    .setExpirationTime(expirationTime)
    .setProtectedHeader({
      alg: ALGORITHM,
      typ: 'JWT'
    })
    .sign(privateKey)

  return jwt
}

const getPublicKey = () => {
  return `-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuS+XMVmbcM6s6+1MxNWb
74hTykn0sgNtr6ONZoAxy9QzI34lcNXhxX4OSDJy9OXxDTQgxr/mEDd0k1JwVIUs
cAim/tn/1LGGgXfX8wV+hVIt4DB9dQS07NfGj9gaGoVmKTA6upTBZnVEl9zd7wKv
Eoe5IAEhzUHB6MPmhX/AYvRNChH/QwY7m44d5xYr/PR3gB0w16kOTVD0or6rBykJ
HohOnD78xRq9tD20ll2oYogpAO8/ru2Cd6qMZ4zaqDlwMJxB/yPRaWpL5ipwOf9n
XSH3nd6xmwPwSPnhrfx5LbEnNYUzrE/OVP5VkGkObKF5XrFmYfQVDRd9pbkVxGaA
OBcIyD/qHrjwJUN8KkIsmaDLNmZTnz2RgN1jo/CIKF26sRJD/BGLQmNlLSFjR0pq
PvonneJl1ErcTXfSSnqecWmFMfoLeJvGwArx//5bK9X73ZGB550BLywe+0SBR7/0
oST0TVOO8dsSQ0KFllo00nem5aoJTsGE04VPt7P6YDrYBC8UKBjryoO5C+yGUp7k
oOIrrebnYfaMKr5Z1+IlI+OSEK5fE+X24CQeSn4BryUvX+zOE2TyM18KBSxTK9IE
Qr3OVi2uCbqPUq7TPexy9eI4YTbTcZzVT37dnFa1ac9RWTgVHG3K6cvagShhE71Y
oURbnb8ZbUUx8d5/hx+krl0CAwEAAQ==
-----END PUBLIC KEY-----`  
}

const getWrongPublicKey = () => {
  return `-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAi6rqL4i0UOE/Xl0DZ5qm
TaNC+Nxd+q6grVfyz77kOx0K3xtFbroqf8O4rpFwqaxI3sfa/g9C6RYIABmeRg1v
r1hNWrdTerGVuIjrPqCQ1YdNxywyPH3kaXgh4o4NpC76KUmeLG7nD1pc1ia6WBDg
c19XMqAZZwX8KCJcro5I1pfMpX3vE42jeBudWhFEym079P8HIVZom8sT+/5DJgP5
iE/GK2ykuwgEsbUTYno90Y+lOAsomBSCo0R/lzBoV53yYAQyp4xA2K1V2p1r3Q5q
D/qEtmNltl1YLobMMGMCEtR58ZqHjHrF13WTVNsx2pxmAxZeOCQwhxKPFN4O7v7W
n7SsTA7MbIFLrqhudwacEKPLsc7jYwQhhzUj51hQqwRBhY0Kj6sHpR031hMsJwjS
bOG/A3Yoi4W4hPkvmnlKT2HncUbfWcSy3unUmvePMmZcgMscLgXWZVBW/qlJWwEP
LkHj2WsaIz0ZMt3mIrlZIS8xHSPYqcv4cqzrqAiCflG2ZFUtZbtU0a/NrNn80iGZ
iycpvuAAypSjrGJkve6hSH+ZwfyM6Cxtx8O1HhmX8gU+GciT8GBxwmmuObsP3jg5
OwzCG9ZFMDeQCFSjGhVzEGy043Ap/yfb8y1XtON9v/V9mSbw+70ZGdAG1x8SHSSe
R0XSaOOjxbJtkwiN4m3p9UUCAwEAAQ==
-----END PUBLIC KEY-----`
}


test('verifies JWT', async () => {
  const spki = getPublicKey();
  const publicKey = await importSPKI(spki, ALGORITHM);
  
  const jwt = await createJWt()
  const { payload, protectedHeader } = await jwtVerify(jwt, publicKey, {
                                                      algorithms: ["RS256"]
                                                    });

  expect(payload['urn:example:claim']).toBe(true);
  expect(payload.exp).toBeDefined();
});


test('fails to verify signature when using the wrong public key', async () => {
  const spki = getWrongPublicKey();
  const publicKey = await importSPKI(spki, ALGORITHM);
  
  const jwt = await createJWt()

  await expect(jwtVerify(jwt, publicKey, {algorithms: ["RS256"]}))
    .rejects
    .toThrow(JWSSignatureVerificationFailed)
});


test('throws JWTExpired when token is past expiration', async () => {
        const spki = getPublicKey();
        const publicKey = await importSPKI(spki, ALGORITHM);
        
        const jwt = await createJWt(/*createExpiredJwt:*/ true); 

        await expect(jwtVerify(jwt, publicKey))
            .rejects
            .toThrow(JWTExpired);
});


test('throws JWSInvalid when token is malformed', async () => {
        const spki = getPublicKey();
        const publicKey = await importSPKI(spki, ALGORITHM);
        
        const malformedToken = "this.is.not.a.token";

        await expect(jwtVerify(malformedToken, publicKey))
            .rejects
            .toThrow(JWSInvalid);
});