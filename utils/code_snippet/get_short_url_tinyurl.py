
import requests

def get_shorturl(token, url):
    response = requests.post("https://api.tinyurl.com/create",
                  headers={'Authorization': token},
                  data={'url':url})
    return response.json()

token = ''
