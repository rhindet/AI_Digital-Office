from pwdlib import PasswordHash


from datetime import datetime, timedelta, timezone
from jose import jwt

from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

## jwt
SECRET_KEY = "cambiar-esto-mas-adelante"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
        data:dict,
        expires_delta: timedelta | None= None,
) -> str :
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=15)
        )

    to_encode.update({
         "exp":expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

