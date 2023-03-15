from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate, create_access_token
from models import Token

EXPIRATION_MINUTES = 300

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Função que fornece verifica o login do usuário e fornece o JWToken.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Dados de logins.

    Raises:
        HTTPException: Credenciais de acesso incorretas.

    Returns:
        Token: JWToken codificado.
    """
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = form_data.scopes if form_data.scopes else user.scopes
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expiration_minutes=EXPIRATION_MINUTES,
    )
    return access_token
