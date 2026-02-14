from fastapi import Header, status
from api_models import HTTPError

"""
This file contains the documentation of each endpoint of auth_api.py
"""

# https://fastapi.tiangolo.com/advanced/additional-responses/
# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/

COMMON_ERRORS = {
    # Fast API creates the 422 (Validation Error) automatically.
    503: {"description": "Downstream service unavailable", "model": HTTPError}
}

JWT_AUTH_HEADER = Header(
    None, 
    description="**Required**. JWT Token with `Bearer ` prefix.", 
    example="Bearer <JWT_TOKEN>"
)


SIGNUP_DOC = {
    "status_code": status.HTTP_201_CREATED,
    "tags": ["Authentication"],
    "summary": "Register a new user",
    "description": "Creates a new user with a **unique username** and password.",
    "openapi_extra": {
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "username": "JohnDoe",
                        "password": "securePassword123"
                    }
                }
            }
        }
    },
    "responses": {
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "JohnDoe",
                        "message": "User created successfully"
                    }
                }
            }
            
            },
        409: {"description": "Username already exists", "model": HTTPError},
        **COMMON_ERRORS
    },
}

LOGIN_DOC = {
    "status_code": status.HTTP_200_OK,
    "tags": ["Authentication"],
    "summary": "Login and get Token",
    "description": "Validates credentials and returns a **JWT Bearer Token**.",
    "openapi_extra": {
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "username": "JohnDoe",
                        "password": "securePassword123"
                    }
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Login successful, returns JWT",
            "content": {
                "application/json": {
                    "example": {
                        "username": "JohnDoe",
                        "message": "Login successful",
                        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkpvaG5Eb2UiLCJleHAiOjE3NzEwODEwNDgsImlhdCI6MTc3MTA3OTI0OH0.jPUWPpkrjhGbNtX77R6KcURjVF6apbpjWuEMMoLpcOj-OJ-Ku2ob1KrLQCtfjyzgM-SclHQCI2YWFhnhbpohc-MYX3HUxIeRc9wrTV8zo-zPK7aQF_hNI7FQbxmhVBPvP51KrAA54HxjpqgQLpmDVGLq_4EymdjcqKkDo7iMPOIXsNfhBN9yvZszc16a4RuU_Y8Jv2kvAXXqB-zDKfkzx43xuDiOvJvpLb3tMdXfYfj0bQTSafmUQRe94jcshyGJcF-d1boyKx5SN5sIG_dJeWpXBg_VBiQhFhDrIei0JA0em6S7wHDdjkBS-8AR0synrSZnCdZFQawAZ44mdkYqoays1GyGL9KPdFDjHP_xZhLYAUYMN29M2wMjNrjjdnPVNt30jfs4jdD503cHNNdQ3Cv9se8QNfeKBGi7h7B70zNaxsHpOJHyEMOs9xjawW2O8MNTpl4uyx-RBbbaQO9LLIZQ7_Rd2RE5qEsO3V8mQ_PtACSvsklto5vPU2VJPjartRvUtjeGaysGw81MJCw95Tr7kO2_5sFtIlxQc_6ENJ59TpLWu-tUe6qQuAY18-glPRS_ovAQpCmqGrUlxG75gU_eO0kCdoPeXphm3e86-hrcqytxBNvghceBGncBi-VPO6yuIvunaKvY_Eymvbo8f2j8HCwbSpZdNevm38nDZtA",
                        "tokentype": "bearer"
                    }
                }
            }
        },
        401: {"description": "Incorrect username or password", "model": HTTPError},
        **COMMON_ERRORS
    }
}

DELETE_ACCOUNT_DOC = {
    "status_code": status.HTTP_200_OK,
    "tags": ["Account Management"],
    "summary": "Delete User Account",
    "description": "Permanently removes the user. Requires **Password confirmation** and **Bearer Token**.",
    "openapi_extra": {
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "password": "securePassword123"
                    }
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Account deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Account for user 'John Doe' has been successfully deleted.",
                    }
                }
            }

        },
        401: {"description": "Unauthorized (Invalid Token or Wrong Password)", "model": HTTPError},
        **COMMON_ERRORS
    }
}