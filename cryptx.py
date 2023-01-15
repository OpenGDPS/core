import base64
import hashlib

def base64_decode(text: str) -> str:
    """Encodes the param `text` using url safe Base64.
    Args:
        text (str): The text that is to be encoded using Base64.
    Returns:
        Base64 encoded string.
    """

    # This is simply a wrapper around base64 functions.
    return base64.urlsafe_b64decode(text.encode()).decode()

def base64_encode(text: str) -> str:
    """Encodes the param `text` using url safe Base64.
    Args:
        text (str): The text that is to be encoded using Base64.
    Returns:
        Base64 encoded string.
    """

    # This is simply a wrapper around base64 functions.
    return base64.urlsafe_b64encode(text.encode()).decode()

def sha1_hash(text: str) -> str:
    """Hashes a plaintext string in the SHA1 hashing algorhythm.
    Args:
        text (str): The text to hash.
    Returns:
        `string` hashed in SHA1.
    """

    return hashlib.sha1(text.encode()).hexdigest()