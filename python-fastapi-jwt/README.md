# API Python com JWT

---

Esse projeto foi criado para moldar uma implantação de API usando Python que autentica o usuário e valida os acesso depois usando o padrão OAuth 2.0 com Json Web Token (JWT) assinado.

---

## Requisitos

Esse projeto tem as seguintes bibliotecas como requisito:

### Código Fonte
- python-jose
- fastapi
- pydantic

### Webserver
- uvicorn

---

## Modulos

main.py: Modulo principal da FastAPI, inicia a raiz dos endpoints.
auth.py: Modulo que faz a autenticação do usuário, criação, decodificação e validação do JWT.
models.py: Armazena o modelos de dados.
routers/authentication.py: Endpoint de autenticação e token.
routers/users.py: Endpoint de usuários. Usa como dependencia a validação dos tokens.

## Utilizando

- Implemente a autenticação na função authenticate do arquivo auth.py e ela precisa retornar o modelo User com os campos obrigatórios username e scopes.
- Altere o modelo do TokenData para os dados pertinentes a sua aplicação.