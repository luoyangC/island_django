import json
import requests

from config.settings import API_KEY


s = requests.session()


def talk(content, username):
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "perception": {
            "inputText": {"text": content}
        },
        "userInfo": {
            "apiKey": API_KEY,
            "userId": username
        }
    }
    data = json.dumps(data)
    r = s.post(url, data=data)
    r = json.loads(r.text)
    code = r['intent']['code']
    if code < 10000:
        result = '抱歉，不知道你在说什么(+_+)'
    else:
        result = ''.join([i['values']['text'] for i in r['results']])
    return result
