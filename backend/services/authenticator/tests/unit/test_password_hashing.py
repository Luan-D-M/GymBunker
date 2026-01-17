import pytest
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

# See authenticator/postgre/init.sql
DB_VARCHAR_LENGTH_FOR_STORING_PASSWORD_HASH = 200

@pytest.fixture
def hasher():
    """Provides a PasswordHasher instance."""

    return PasswordHasher()

@pytest.fixture
def mock_password():
    """Provides a mock password."""

    return "Mock password."


def test_successful_hashing_and_verifying(hasher, mock_password):
    hashed_password_string = hasher.hash(mock_password)

    # Raises a exception if verification fails for any reason.
    hasher.verify(hashed_password_string, mock_password)  


def test_argon2_salt_produces_different_hashes_for_same_password(hasher, mock_password):
    hashed_password_1 = hasher.hash(mock_password)
    hashed_password_2 = hasher.hash(mock_password)

    assert hashed_password_1 != hashed_password_2, \
        "Hashing the same password twice should produce different hash strings due to unique salts."


def test_hashed_output_size_within_db_limit(hasher, mock_password):
    hashed_password_string = hasher.hash(mock_password)

    assert len(hashed_password_string) <= DB_VARCHAR_LENGTH_FOR_STORING_PASSWORD_HASH, \
        f"Generated hash length ({len(hashed_password_string)}) exceeds DB limit." 
    

def test_incorrect_password_raises_VerifyMismatchError(hasher, mock_password):
    fake_password = "A fake password."
    hashed_password_string = hasher.hash(mock_password)

    with pytest.raises(VerifyMismatchError):
        hasher.verify(hashed_password_string, fake_password)


@pytest.mark.parametrize(
    "invalid_hash",
    [
        ("_not_an_argon2_hash"),
        ("$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ"),
        ("$argon2id$v=19$m=65536,t=3,p=4$salt_with_invalid_char!$y2E3X/b7kvZ7bEc1nE0Log"),
        ("$argon2id$v=19$m=65536,t=3,p=4$U/p6wTQ1VrhTI/jpWYGlsA$ikYkyzCZPQ1REvbYcv1CNvq5/P422XXS9f5utMkiCw!")
    ],
    ids=[ 
        "Nonsense_string",
        "without_hash_digest",
        "invalid_char_in_salt_part",
        "invalid_char_in_hash_part"
    ]
)
def test_verify_malformed_hash_raises_InvalidHash_or_VerificationError(hasher, invalid_hash, mock_password):
    """
    InvalidHashError: If hash is so clearly invalid, that it couldn't be passed to Argon2.
    VerificationError: If verification fails for other reasons.

    https://argon2-cffi.readthedocs.io/en/stable/api.html
    """

    with pytest.raises((InvalidHash, VerificationError)):
        hasher.verify(invalid_hash, mock_password)