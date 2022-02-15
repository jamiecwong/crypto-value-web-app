import json
import traceback
from typing import Union

import requests
from flask import Flask, render_template
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = Flask(__name__)

coin_id = "bitcoin"
currency = "usd"


@app.route("/", methods=["GET"])
def main() -> str:
    return render_template("index.html", display_text=get_display_text())


def get_display_text() -> str:
    result = get_coin_value(coin_id, currency)
    if isinstance(result, int):
        display_text = (
            f"{coin_id.title()} value is {result} {currency.upper()}"
        )
    elif isinstance(result, str):
        display_text = f"Application error: {result}"
    return display_text


def get_coin_value(coin_id, currency) -> Union[int, str]:
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


def get_response(coin_id, currency) -> str:
    s = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[502, 503, 504]
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = dict(ids=coin_id, vs_currencies=currency)
    response = s.get(url, params=params)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
