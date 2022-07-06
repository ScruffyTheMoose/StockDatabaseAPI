from pandas import DataFrame, Series
from yahoo_fin import stock_info as si


def get_sp500_tickers() -> list:
    """
    Returns list of all tickers in the SP500
    """

    return si.tickers_sp500()


def get_full_hist(ticker: str) -> DataFrame:
    """
    Returns a DataFrame of the full HLOCV history for ticker
    """

    data = si.get_data(ticker=ticker)
    data.drop(["adjclose", "ticker"], axis=1)

    return data


def get_range_hist(ticker: str, start: str, end: str) -> DataFrame:
    """
    Returns a DataFrame of the HLOCV history for ticker over designated date range
    """

    data = si.get_data(ticker=ticker, start_date=start, end_date=end)
    data.drop(["adjclose", "ticker"], axis=1)

    return data


def get_single_hist(ticker: str, date: str) -> Series:
    """
    Returns a Series of the HLOCV history for ticker on a specified date
    """

    data = si.get_data(ticker=ticker, start_date=date, end_date=date)
    data.drop(["adjclose", "ticker"], axis=1)

    return data
