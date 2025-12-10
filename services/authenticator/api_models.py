from pydantic import BaseModel

class UserSignUp(BaseModel):
    username: str
    password: str

class UserLogIn(BaseModel):
    username: str 
    password: str

class UserDeleteAccount(BaseModel):
    password: str