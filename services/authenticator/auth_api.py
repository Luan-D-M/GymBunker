from fastapi import FastAPI, Depends, status, Header, HTTPException
from fastapi.responses import JSONResponse
from api_models import UserSignUp, UserLogIn, UserDeleteAccount
from dependencies import get_auth_manager, get_jwt_util, get_public_key
from auth_manager import AuthManager
from jwt_utils import JWTUtil
from grpc_client import create_user, delete_user

app = FastAPI()

@app.post('/signup')
async def signup(
    user: UserSignUp,
    auth_manager: AuthManager = Depends(get_auth_manager),
):
    is_username_taken = await auth_manager.username_exists(user.username)
    if is_username_taken:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    await auth_manager.hash_password_and_store_user_in_database(
        user.username, user.password
    )
    try:
        await create_user(user.username)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Clean up the local DB so the user can try again later
        await auth_manager.delete_user(user.username)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {e}" # <--- Add {e} temporarily to the response
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "username": user.username,
            "message": "User created successfully",
        }
    )


@app.post('/login')
async def login(
    user: UserLogIn,
    auth_manager: AuthManager = Depends(get_auth_manager),
    jwt_util: JWTUtil = Depends(get_jwt_util),
):
    is_authenticated = await auth_manager.verify_password_and_update_its_hash_in_database_if_needed(
        user.username, user.password
    )
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    jwt_token = jwt_util.create_token(user.username)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "username": user.username,
            "message": "User created successfully",
            "access_token": jwt_token,
            "tokentype": "bearer"
        }
    )


@app.post('/delete-account')
async def delete_account(
    user: UserDeleteAccount,
    authorization: str = Header(None),
    auth_manager: AuthManager = Depends(get_auth_manager),
    jwt_util: JWTUtil = Depends(get_jwt_util),
    public_key: bytes = Depends(get_public_key)
):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header is not valid.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    jwt_token = authorization.split(" ")[1]
    token_data = jwt_util.verify_token(jwt_token, public_key)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not await auth_manager.username_exists(token_data["username"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    valid_credentials = await auth_manager.verify_password_and_update_its_hash_in_database_if_needed(
        token_data["username"], user.password
    )

    if not valid_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    await auth_manager.delete_user(token_data["username"])
    try:
        await delete_user(token_data["username"])
    except Exception as e:
        # Doesnt raise an error here because the account is effectively deleted for the user.
        pass
        # ToDo: Logging? Queue for deletion later?

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Account for user '{token_data['username']}' has been successfully deleted."}
    )