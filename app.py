


#This example uses Python 2.7 and the python-request library.

import requests
import json
import traceback
import random

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask import Flask, request, render_template



app = Flask(__name__)

coin_id = "bitcoin"
currency = "usd"


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html', display_text=get_display_text())


def get_display_text():
    result = get_coin_value(coin_id, currency)
    if isinstance(result, int):
        display_text = f"{coin_id.title()} value is {result} {currency.upper()} - {random.randint(0,9)}"
    elif isinstance(result, str):
        display_text = f"Application error: {result}"
    return display_text


def get_response(coin_id, currency):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    url = f"https://api.coingecko.com/api/v3/simple/price"

    params = dict(
        ids=coin_id,
        vs_currencies=currency
    )
    response = s.get(url, params=params)
    return response


def get_coin_value(coin_id, currency):
    try:
        response = get_response(coin_id, currency)
        response = json.loads(response.text)
        value = int(response[coin_id][currency])
        return value

    except requests.exceptions.TooManyRedirects:
        text = "Too  many redirects, is the URL correct?"
        return text
    except requests.exceptions.RequestException as e:
        text = str(e)
        return text
    except Exception:
        text = str(traceback.format_exc())
        return text


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #TODO REMOVE DEBUG
    app.run(debug=True, host='0.0.0.0')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
