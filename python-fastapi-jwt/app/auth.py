from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from config import Phrases
from models import Token, TokenData, User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={
        "admin": "Systema Admin with god power",
        "user": "General users with limited power",
    },
)

PVK = Phrases.load_pvk_file()
PBK = Phrases.load_pbk_file()


def authenticate(username: str, password: str) -> User:
    """Autentica o usuário e retorna os scopes de privilegio

    Args:
        username (str): Nome do usuário
        password (str): Senha do usuário

    Returns:
        User: Info do usuário contido no banco
    """
    if username == "eu" and password == "eu":
        return User(username="eu", scopes=["user"])
    elif username == "admin" and password == "admin":
        return User(username="admin", scopes=["admin"])
    return None


def create_access_token(data: dict, expiration_minutes: int) -> Token:
    """Generate JW Token

    Args:
        sub (str): Subject Username
        exp (int): Token Expiration Time

    Returns:
        str: JW Token
    """
    data["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=expiration_minutes)
    token = jwt.encode(data, PVK, algorithm="RS256")
    return Token(access_token=token, token_type="bearer")


def decode_access_token(token: str) -> TokenData:
    """Decode Token

    Args:
        token (str): JWToken RS256 Encoded

    Returns:
        dict: Decoded Payload
    """
    token_decoded = jwt.decode(token, PBK, algorithms=["RS256"])
    return TokenData(sub=token_decoded.get("sub"), scopes=token_decoded.get("scopes"))


async def verify_privileges(
    security_scopes: SecurityScopes, token=Depends(oauth2_scheme)
) -> TokenData:
    """Verifica o token e os privilegios do usuários

    Args:
        security_scopes (SecurityScopes): Lista de scopos permitidos do Path
        token (TokenData, optional): Dados do Token decodificado e assinado.

    Raises:
        ExpiredSignatureError: Erro de token expirado.
        JWTError: Demais erros de token.
        HTTPException: Erro de credencial não autorizada.
    Returns:
        TokenData: Dados decodificados do JWToken.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        token_data = decode_access_token(token)
        if token_data.sub is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                credentials_exception.detail = "Privilegios insuficientes."
                raise credentials_exception
    except ExpiredSignatureError:
        credentials_exception.detail = "Token expirado."
        raise credentials_exception
    except JWTError:
        credentials_exception.detail = "Token invalido."
        raise credentials_exception
    return token_data
