import json
import re
from datetime import datetime

import pymongo


def configure_download():
    userMongo = 'bi-mktplace'
    passwordMongo = '*********'
    collection_str = 'BureauTransactions'
    query = { "FullProposalId": { "$in": fps}, "BureauScoreModelId": {"$in": bureaus}}
    fields = '_id,_t,BureauScoreModelId,CPF,InvestorId,FullProposalId,RequestDate'
    data_dump = r'./{}.json'.format(collection_str)

    download_data(userMongo, passwordMongo, collection_str, fields, query, data_dump)


def datetime_converter(obj):
    if isinstance(obj, datetime):
        return obj.__str__()


def remove_special_character(obj):
    for key in list(obj.keys()):
        new_key = re.sub('[^a-zA-Z0-9\_]', '_', key)
        if new_key != key:
            obj[new_key] = obj[key]
            del obj[key]
    return obj


def download_data(userMongo, passwordMongo, collection_str, fields, query, data_dump):
    client = pymongo.MongoClient(f"mongodb+srv://{userMongo}:{passwordMongo}@cluster-01.tcqut.mongodb.net/credmarket?retryWrites=true&w=majority")
    db = client.credmarket
    collection = db[collection_str]

    with open(data_dump, 'w') as file:
        projection = {field: 1 for field in fields.split(',')}
        linhas = collection.find(query,projection)
        for linha in linhas:
            doc_aux1 = json.dumps(linha,default=datetime_converter)
            doc_aux2 = json.loads(doc_aux1, object_hook=remove_special_character)
            file.write(json.dumps(doc_aux2) + '\n')

            
if __name__ == '__main__':
    configure_download()
