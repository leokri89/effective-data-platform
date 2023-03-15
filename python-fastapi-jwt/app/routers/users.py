from fastapi import APIRouter, Depends, Security

from auth import verify_privileges
from models import TokenData, User

router = APIRouter()


async def get_current_user(token_data: TokenData = Depends(verify_privileges)):
    """Retorna o modelo User do usuário atual.

    Args:
        token_data (TokenData, optional): Dados armazenados no Token. Tem dependencia da validação dos privilegios (verify_privileges).

    Returns:
        User: informações do usuário
    """    
    user = User(username=token_data.sub, scopes=token_data.scopes)
    return user


@router.get("/me", response_model=User)
async def get_user_me(user: User = Security(get_current_user, scopes=["user"])):
    """Retorna quem está logado.

    Returns:
        User: Retorna o usuário logado.
    """
    return user
