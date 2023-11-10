from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

hasher = PasswordHasher()


def hash_pw(password: str) -> str:
    return hasher.hash(password)


def password_compare(db_pw_hash, password) -> bool:
    """
    Compare a database password hash to a plaintext password
    # TODO Pull password from the database by user so we can re hash if need be
    :param db_pw_hash: argon2 DB hash from our database
    :param password: plaintext oassword that comes form a request
    :return: boolean
    """
    verified = False
    try:
        verified = hasher.verify(db_pw_hash, password)
    except (InvalidHashError, VerifyMismatchError):
        # To warn log user/attempt
        pass
    else:
        if hasher.check_needs_rehash(db_pw_hash):
            # Todo when we have DB
            pass

    return verified
