from hashlib import pbkdf2_hmac


def derive_vault_key(username: str,
                     password: str,
                     salt: bytes,
                     iterations: int = 700_000,
                     hash_name: str = "sha256",
                     encoding: str = "utf-8",) -> str:
    """
    Derives a vault key from a username and password combination.
    
    Takes username and password as parameters, as well as iterations of hashing.
    """
    
    return pbkdf2_hmac(hash_name, f"{username}{password}".encode(encoding), salt, iterations).hex()


def derive_auth_key(vault_key: str,
                    password: str,
                    salt: str,
                    iterations: int = 100_000,
                    hash_name: str = 'sha256',
                    encoding: str = 'utf-8') -> str:
    """
    Appends vault key to password, hashes for 'n' iterations and returns result
    """
    return pbkdf2_hmac(hash_name, f"{vault_key}{password}".encode(encoding), salt, iterations).hex()