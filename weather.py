import requests
from flask import Flask

app = Flask(__name__)

API_KEY = 'oops'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?zip={},GB&mode=json&units=metric&appid={}'

def query_api(zip):
    try:
        data = requests.get(API_URL.format(zip, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

@app.route('/weather/<zip>')
def result(zip):
    resp = query_api(zip)

    try:
        text = resp['name'] + ' temperature is ' + str(resp['main']['temp']) + ' degrees celcius.'
    except:
        text = 'not a valid postcode <br> can only be the first half'
    
    return text

if __name__ == '__main__':
    app.run(debug=True)