import sys

class PublicKey:
    e: int
    n: int

class PrivateKey:
    d: int
    n: int

def frombytes(bytes: bytes):
    """Internal function, should not be used

    Args:
        bytes (bytes): _description_

    Returns:
        _type_: _description_
    """
    return int.from_bytes(bytes, sys.byteorder)


def tobytes(_int: int):
    """Internal function, should not be used

    Args:
        bytes (bytes): _description_

    Returns:
        _type_: _description_
    """
    return _int.to_bytes((_int.bit_length() + 7) // 8, sys.byteorder)


class TextbookRSA:
    def __init__(self) -> None:
        pass

    def encrypt(text: bytes, key: PublicKey):
        """Encrypt a text with RSA. Requires a public key.

        Args:
            text (bytes): Text to encrypt
            key (PublicKey): Public key that will be used

        Returns:
            bytestring: byte string of our encrypted text.
        """
        return tobytes(pow(frombytes(text), key.e, key.n))

    def decrypt(text: bytes, key: PrivateKey):
        """Decrypt encrypted text

        Args:
            text (bytes): Byte string representing the encrypted text
            key (PublicKey): Private Key, used for decrypting the text

        Returns:
            bytestring: A bytestring representing the original, unencrypted text.
        """
        return tobytes(pow(frombytes(text), key.d, key.n))