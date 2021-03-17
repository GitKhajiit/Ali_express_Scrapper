import requests


def get_currency_exchage(curr_1, curr_2):
    link = 'https://www.alphavantage.co/query'
    data = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': curr_1,
        'to_currency': curr_2,
        'apikey': '9ZMR2XAF613AP2W7'
    }
    response = requests.get(link, params=data).json()  # take the response in json format
    exchange_rate_str = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    exchange_rate_num = float(exchange_rate_str)

    return round(exchange_rate_num, 2)
