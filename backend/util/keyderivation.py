from hashlib import pbkdf2_hmac


def derive_auth_key(authkey: str,
                    salt: str,
                    iterations: int = 100_000,
                    hash_name: str = 'sha256',
                    encoding: str = 'utf-8') -> str:
    """
    Appends vault key to password, hashes for 'n' iterations and returns result
    """
    return pbkdf2_hmac(hash_name, authkey.encode(encoding), salt, iterations).hex()
