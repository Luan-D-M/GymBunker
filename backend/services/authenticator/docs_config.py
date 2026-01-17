from fastapi import status

"""
This file contains the documentation of each endpoint of auth_api.py
"""

COMMON_ERRORS = {
    422: {"description": "Validation Error (Bad input format)"},
    503: {"description": "Downstream service unavailable"}
}

SIGNUP_DOC = {
    "status_code": status.HTTP_201_CREATED,
    "tags": ["Authentication"],
    "summary": "Register a new user",
    "description": "Creates a new user with a **unique username** and password.",
    "responses": {
        201: {"description": "User created successfully"},
        409: {"description": "Username already exists"},
        **COMMON_ERRORS
    }
}

LOGIN_DOC = {
    "status_code": status.HTTP_200_OK,
    "tags": ["Authentication"],
    "summary": "Login and get Token",
    "description": "Validates credentials and returns a **JWT Bearer Token**.",
    "responses": {
        200: {"description": "Login successful, returns JWT"},
        401: {"description": "Incorrect username or password"},
        422: {"description": "Validation Error"}
    }
}

DELETE_ACCOUNT_DOC = {
    "status_code": status.HTTP_200_OK,
    "tags": ["Account Management"],
    "summary": "Delete User Account",
    "description": "Permanently removes the user. Requires **Password confirmation** and **Bearer Token**.",
    "responses": {
        200: {"description": "Account deleted successfully"},
        401: {"description": "Unauthorized (Invalid Token or Wrong Password)"},
        422: {"description": "Missing required fields"}
    }
}