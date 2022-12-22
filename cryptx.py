import base64

def base64_encode(text: str) -> str:
    """Encodes the param `text` using url safe Base64.
    Args:
        text (str): The text that is to be encoded using Base64.
    Returns:
        Base64 encoded string.
    """

    # This is simply a wrapper around base64 functions.
    return base64.urlsafe_b64encode(text.encode()).decode()