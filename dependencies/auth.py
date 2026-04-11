from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import UnauthorizedException
from utils.jwt_tokens import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    payload = decode_access_token(token)
    if payload is None:
        raise UnauthorizedException("Token inválido o expirado")
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedException("Token sin sujeto")
    return str(sub)
