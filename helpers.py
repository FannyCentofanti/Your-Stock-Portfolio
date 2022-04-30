import pyEX
from flask import session, redirect
from functools import wraps
from config import api_key

# set API_KEY
iexcloud_api = pyEX.Client(
    api_token=api_key, version='stable')

def get_stock_price(symbol):
    """Get the latest price of the stock"""

    # get stock prices for the company with this symbol input
    try:
        response = iexcloud_api.quote(symbol=symbol)
    except:
        return None

    # save the latest price of the stock to variable price
    price = response['latestPrice']

    return price


def get_stock_info(symbol):
    """Get information of the stock"""

    # contact API to get information of the company with the input symbol
    try:
        response = iexcloud_api.company(symbol=symbol)
    except:
        return None

    # return the response from the API-request, with the information of interest
    try:
        if response['companyName'] == None:
            return None
        else:
            return {
                "symbol": response['symbol'],
                "name": response['companyName'],
                "industry": response['industry'],
                "sector": response['sector']
            }
    except:
        print("could not print info about stock")
        return None


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def contains(list, filter):
    """Check if list contains a certain filter."""

    for x in list:
        if filter(x):
            return True
    return False


def get_display_data():
    """Create some data for display on the website."""

    display_data_info = [
        {"symbol": "AAPL", "shares": "70"}, # manufacturing
        {"symbol": "TSLA", "shares": "100"}, # manufacturing
        {"symbol": "JPM", "shares": "200"}, # finance (mastercard)
        {"symbol": "WPC", "shares": "80"}, # buildings 
        {"symbol": "AMZN", "shares": "30"}, # retail trade
        {"symbol": "AMRC", "shares": "120"}, # Energy
        {"symbol": "SNPS", "shares": "110"}, # Tech
        {"symbol": "FB", "shares": "90"} # information
    ]

    return display_data_info
