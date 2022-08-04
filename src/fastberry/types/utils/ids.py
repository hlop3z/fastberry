"""
    * ID (Encoder || Decoder)
"""

import base64
import hashlib


def encode(text):
    """[summary]
    Base64 Encoder.

    Args:
        text (str): String to be encoded.

    Returns:
        str: base64.urlsafe_b64encode
    """
    fill_up = hashlib.blake2s(f"{text}".encode("utf-8"), digest_size=8).hexdigest()
    text = f"{ text }::{ fill_up }"
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8")


def decode(text):
    """[summary]
    Base64 Decoder.

    Args:
        text (str): String to be decoded.

    Returns:
        str: base64.urlsafe_b64decode
    """
    code = base64.urlsafe_b64decode(text.encode("utf-8")).decode("utf-8")
    text = code.split("::")
    return text[0]


class ID:
    """[summary]
    ID (Encoder || Decoder)
    """

    @staticmethod
    def encode(keys):
        """Encode-Wrapper"""
        try:
            if not isinstance(keys, list):
                return encode(keys)
            return [encode(key) for key in keys]
        except Exception as error:
            raise Exception("Invalid ID") from error

    @staticmethod
    def decode(keys):
        """Decode-Wrapper"""
        try:
            if not isinstance(keys, list):
                return decode(keys)
            return [decode(key) for key in keys]
        except Exception as error:
            raise Exception("Invalid ID") from error


def sql_id_decode(unique_id) -> int | None:
    """Decoder for SQL"""
    try:
        return_value = int(ID.decode(unique_id))
    except Exception:
        return_value = None
    return return_value
