from pydantic import BaseModel, Field

class UserSignUp(BaseModel):
    username: str = Field(
        ...,  # Means this field has no default value, so it is mandatory.
        min_length=3, 
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$", 
        description="Username must be 3-30 chars and alphanumeric only"
    )
    password: str = Field(
        ..., 
        min_length=4,
        max_length=64,
        description="Password must be 4-64 chars long"
    )
class UserLogIn(BaseModel):
    username: str 
    password: str

class UserDeleteAccount(BaseModel):
    password: str

class HTTPError(BaseModel):   # Used by documentation
    detail: str