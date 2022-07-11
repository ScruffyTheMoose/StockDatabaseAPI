from urllib import response
import requests, json


def get_tickers() -> list:
    reqURL = "localhost:5000/tickers"
    response = requests.get(reqURL)
    data = response.json()["tickers"]

    return data


def drop_ticker(ticker: str) -> requests.Response:
    reqURL = "localhost:5000/tickers"
    req_data = {"ticker": ticker}

    response = requests.delete(reqURL, data=json.dumps(req_data))

    return response


def create_ticker(ticker: str) -> requests.Response:
    reqURL = "localhost:5000/tickers"
    req_data = {"ticker": ticker}

    response = requests.post(reqURL, data=json.dumps(req_data))

    return response


def post_data(
    ticker: str,
    date: str,
    high: float,
    low: float,
    open: float,
    close: float,
    volume: int,
) -> requests.Response:

    reqURL = "localhost:5000/tickers"
    req_data = {
        "ticker": ticker,
        "date": date,
        "high": high,
        "low": low,
        "open": open,
        "close": close,
        "volume": volume,
    }

    response = requests.post(reqURL, json.dumps(req_data))

    return response
