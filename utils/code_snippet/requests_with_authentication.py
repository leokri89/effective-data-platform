
import requests
import json
import datetime

login_url = "https://engine.bompracredito.com.br/api/CredMarketApi/Login"
authenticated_url = "https://ckqry.bompracredito.com.br/milestoneStats"

payload = json.dumps({"user": "*", "password": "*"})
headers = { 'Content-Type': 'application/json' }

with requests.Session() as sesh:
    response = sesh.post(login_url, data=payload, headers=headers)
    session_id = json.loads(response.text).get('sessionId')

    payload = json.dumps({"match": {"DayMonthYear": {"$gte": "2021-06-01"}},"InvestorId": 1})
    headers = { 'session-id': session_id,'Content-Type': 'application/json' }

    response = requests.request("POST", authenticated_url, headers=headers, data=payload, verify=False)

    data = json.loads(response.text)
