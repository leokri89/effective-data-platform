from bson.json_util import dumps
import pymongo
from faker import Faker


def gen_profile():
    fake = Faker(["pt-BR"])
    fields = ["name", "username", "sex", "mail"]
    profile = fake.profile()
    return {field: profile[field] for field in fields}


def get_database_connection():
    url = "mongodb+srv://delk-user:delk-user@atlante.qcgiw.mongodb.net/mockDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(url)
    db = client.mockDatabase
    return db


def lambda_handler(event, context=None):
    try:
        if event.get('qtd_user') > 0:
            db = get_database_connection()
            count_inicial = db.profile.count_documents({})

            lista_criados = []
            for x in range(event.get('qtd_user')):
                profile = gen_profile()
                db.profile.insert_one(profile)
                lista_criados.append(profile)

            count_final = db.profile.count_documents({})
            return { "status": 200, "qtd users criados":count_final-count_inicial, "criados": dumps(lista_criados)}
        elif event.get('qtd_user') == 0:
            return { "status": 200, "err": 'qtd_user precisa ser superior a zero'}
        else:
            return { "status": 200, "err": 'Erro inesperado'}
    except:
        return { "status": 200, "err": 'Erro inesperado'}