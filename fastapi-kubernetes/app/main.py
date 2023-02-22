import redshift_connector
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/redshift/login/{group_name}")
async def login_redshift(user: User, group_name):
    conn = redshift_connector.connect(
        host='redshift.datamart.qa.aws.intranet.pagseguro.uol',
        database='datamart',
        user=user.username,
        password=user.password
    )

    cursor = conn.cursor()
    cursor.execute(f"select data_domain, product_name, group_name, group_type, dat_load from dax_lab.dax_datadomain_products where group_name = '{group_name}'")
    result = cursor.fetchone()
    res_js = {
        "data_domain": result[0],
        "product_name": result[1],
        "group_name": result[2],
        "group_type": result[3],
        "dat_load": result[4].__str__()
    }
    conn.close()
    return {"message": res_js}


@app.post("/dax/user_groups")
async def dax_user_groups(user: User):
    conn = redshift_connector.connect(
        host='redshift.datamart.qa.aws.intranet.pagseguro.uol',
        database='datamart',
        user=user.username,
        password=user.password
    )

    cursor = conn.cursor()
    cursor.execute(f"select * from pg_group")
    result = cursor.fetchall()
    conn.close()
    return {
        "schema": {
                "groname": "string",
                "grosysid": "int",
                "grolist": "list(int)"
            },
        "message": result
        }