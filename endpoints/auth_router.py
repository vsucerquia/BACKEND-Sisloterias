from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.exceptions import UnauthorizedException
from database.database import get_db
from entities.api_usuario import ApiUsuario
from utils.jwt_tokens import create_access_token
from utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(ApiUsuario).filter(ApiUsuario.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise UnauthorizedException("Credenciales incorrectas")
    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer",
    }
