import pytest
import jwt
from datetime import datetime, timedelta, timezone

ALGORITHM = 'HS256'

@pytest.fixture
def secret_key():
    return 'mock-secret-key'

@pytest.fixture
def mock_jwt_token(secret_key):
    payload = {
        'id': 1,
        'user' : 'John Doe',
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=30),
        'iat': datetime.now(timezone.utc)       # iat: Issued At Time
    }

    encoded_jwt = jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


@pytest.fixture
def mock_jwt_expired_token(secret_key):
    payload = {
        'id': 1,
        'user' : 'John Doe',
        'exp' : datetime.now(timezone.utc) - timedelta(minutes=10),
        'iat': datetime.now(timezone.utc) - timedelta(minutes=40)
    }

    encoded_jwt = jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def test_verify_token_success(mock_jwt_token, secret_key):
    decoded_payload = jwt.decode(mock_jwt_token, secret_key, algorithms=[ALGORITHM])
    assert decoded_payload['id'] == 1
    assert decoded_payload['user'] == 'John Doe'

def test_verify_token_expired(mock_jwt_expired_token, secret_key):
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(mock_jwt_expired_token, secret_key, algorithms=[ALGORITHM])

def test_verify_token_failure_because_of_wrong_key(mock_jwt_token):
    fake_key = 'a-fake-key'
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(mock_jwt_token, fake_key, algorithms=[ALGORITHM])

def test_verify_framed_token_generating_invalid_signature(mock_jwt_token, secret_key):
    rubbish= "rubbish_that_generates_invalid_signature"
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(mock_jwt_token + rubbish, secret_key, algorithms=[ALGORITHM])

def test_decode_error_for_malformed_token(secret_key):
    """
    Test a token that clearly is not a valid JWT format (header.payload.signature)
    """
    
    malformed_token_invalid_structure = "this.is.not.a.jwt"
    with pytest.raises(jwt.DecodeError):
        jwt.decode(malformed_token_invalid_structure, secret_key, algorithms=[ALGORITHM])

def test_decode_error_for_bad_base64_encoding(secret_key):
    """
    Test a token with valid structure but invalid base64 encoding in a segment
    with an invalid character in the middle of the token.    
    """

    malformed_token_bad_base64 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid!.signature"
    with pytest.raises(jwt.DecodeError):
        jwt.decode(malformed_token_bad_base64, secret_key, algorithms=[ALGORITHM])

