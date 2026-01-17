import jwt
from datetime import datetime, timedelta, timezone

class JWTUtil:
    """
    Utility class for handling JWT creation and verification.
    
    Note: When using a symmetric algorithm (e.g., HS256), pass the shared secret 
    as the 'private_key' during initialization and as the 'public_key' during verification.
    """


    def __init__(self, private_key_pem_encoded: bytes | str, algorithm: str = "RS256") -> None:
        self.__private_key = private_key_pem_encoded
        self.__algorithm = algorithm


    def create_token(self, username: str, lifetime_in_minutes: int = 30) -> str:
        """
            Create a valid token that expires lifetime_in_minutes minutes after it's creation.
        """

        payload ={
            'username': username,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes=lifetime_in_minutes),
            'iat': datetime.now(timezone.utc)
        }
        encoded_jwt = jwt.encode(payload, self.__private_key, algorithm=self.__algorithm)

        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, public_key_pem_encoded: bytes | str, algorithm: str = "RS256") -> dict | None:
        """
            Verifies the token. Returns the payload if the token is valid, otherwise returns None.
        """
        try:
            payload = jwt.decode(
                token, 
                public_key_pem_encoded, 
                algorithms=[algorithm]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None