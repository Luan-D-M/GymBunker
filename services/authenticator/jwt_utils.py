import jwt
from datetime import datetime, timedelta, timezone

class JWTUtil:


    def __init__(self) -> None:
        #ToDo: Implement opening secretkey by env variable
        self.__secret_key = "default-key"
        self.__algorithm = "HS256"


    def create_token(self, username: str, lifetime_in_minutes: int = 30) -> str:
        """
            Create a valid token that expires lifetime_in_minutes minutes after it's creation.
        """

        payload ={
            'username': username,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes=lifetime_in_minutes),
            'iat': datetime.now(timezone.utc)
        }
        encoded_jwt = jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm)

        return encoded_jwt
    

    def verify_token(self, token: str) -> dict | None:
        """
            Verifies the token. Returns the payload if the token is valid, otherwise returns None.
        """
        try:
            payload = jwt.decode(
                token, 
                self.__secret_key, 
                algorithms=[self.__algorithm]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None