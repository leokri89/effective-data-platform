from fastapi import FastAPI

from routers import authentication, users

app = FastAPI(
    title="DaxTools",
    version="vBeta",
    contact={
        "name": "Data & Analytics",
        "url": "https://docs.dax.com",
        "email": "valinor@pagseguro.com",
    },
)

app.include_router(authentication.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
