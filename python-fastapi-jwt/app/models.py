from typing import List

from pydantic import BaseModel


class User(BaseModel):
    username: str
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    scopes: list[str] = []
