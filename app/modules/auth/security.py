from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['sha256_crypt'])


def hash_password(password: str):
    print(f'PROVIDED PASSWORD {password}')
    return pwd_context.hash(password)
