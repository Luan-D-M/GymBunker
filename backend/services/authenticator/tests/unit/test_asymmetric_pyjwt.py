import pytest
import jwt
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

ALGORITHM = 'RS256'

# --- Fixtures: Key Generation ---
@pytest.fixture(scope="module")
def private_key_pem():
    """Generates a fresh RSA private key for testing."""
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

@pytest.fixture(scope="module")
def public_key_pem(private_key_pem):
    """Extracts the public key from the private key bytes."""
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

# --- Fixtures: Token Generation ---
@pytest.fixture
def mock_rsa_token(private_key_pem):
    """Creates a valid JWT signed with the RSA Private Key."""
    payload = {
        'id': 1,
        'user': 'John Doe',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30),
        'iat': datetime.now(timezone.utc)
    }
    # RSA requires the PRIVATE key to sign
    return jwt.encode(payload, private_key_pem, algorithm=ALGORITHM)

@pytest.fixture
def mock_rsa_expired_token(private_key_pem):
    """Creates an expired JWT signed with the RSA Private Key."""
    payload = {
        'id': 1,
        'user': 'John Doe',
        'exp': datetime.now(timezone.utc) - timedelta(minutes=10),
        'iat': datetime.now(timezone.utc) - timedelta(minutes=40)
    }
    return jwt.encode(payload, private_key_pem, algorithm=ALGORITHM)


# --- Tests ---
def test_verify_rsa_token_success(mock_rsa_token, public_key_pem):
    """
    Validates that a token signed with the Private Key is verified 
    successfully using the Public Key.
    """
    # RSA requires the PUBLIC key to verify/decode
    decoded_payload = jwt.decode(mock_rsa_token, public_key_pem, algorithms=[ALGORITHM])
    
    assert decoded_payload['id'] == 1
    assert decoded_payload['user'] == 'John Doe'

def test_verify_rsa_token_expired(mock_rsa_expired_token, public_key_pem):
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(mock_rsa_expired_token, public_key_pem, algorithms=[ALGORITHM])

def test_verify_rsa_token_failure_wrong_key(mock_rsa_token):
    """
    Ensures that a token signed by Key Pair A cannot be verified by Key Pair B.
    """
    # Generate a completely different key pair
    other_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    wrong_public_key = other_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(mock_rsa_token, wrong_public_key, algorithms=[ALGORITHM])

def test_decode_error_rsa_malformed_token(public_key_pem):
    malformed_token = "not.a.valid.jwt"
    with pytest.raises(jwt.DecodeError):
        jwt.decode(malformed_token, public_key_pem, algorithms=[ALGORITHM])


def test_verify_rsa_token_success_with_string_key(mock_rsa_token, public_key_pem):
    """
    Validates that passing the public key as a STR (instead of bytes) also works.
    This mimics loading a key from an environment variable.
    """
    # Convert bytes -> string
    public_key_str = public_key_pem.decode('utf-8')
    
    # Ensure it is actually a string before testing
    assert isinstance(public_key_str, str)

    # PyJWT should handle the string key automatically
    decoded_payload = jwt.decode(mock_rsa_token, public_key_str, algorithms=[ALGORITHM])
    
    assert decoded_payload['id'] == 1
    assert decoded_payload['user'] == 'John Doe'