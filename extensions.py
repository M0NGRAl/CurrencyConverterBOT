import requests
import json
from config import values

class ConvertEx(Exception):
    pass

class ValuesConvector:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base is quote:
            raise ConvertEx(f'Невозможно перевести одинаковые валюты {base}')
        try:
            base_tic = values[base]
        except KeyError:
            raise ConvertEx(f'Не удалось обработать валюту {base}')
        try:
            quote_tic = values[quote]
        except KeyError:
            raise ConvertEx(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertEx(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://api.currencyapi.com/v3/latest?apikey=cur_live_DB1n5f6ggKXI1SW5QCXp7WGOzkspMtSDAoXbtGQB&currencies={quote_tic}&base_currency={base_tic}')
        data = float(json.loads(r.content)['data'][values[quote]]['value'])
        data *= float(amount)
        return data