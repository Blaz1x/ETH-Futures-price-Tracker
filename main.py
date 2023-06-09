from tradingview_ta import TA_Handler
from datetime import datetime
import requests
import json
import time


def main():
    last_price = []
    while True:
        try:
            ETHUSDT = TA_Handler(
                symbol="ETHUSDT",
                exchange="binance",
                screener="crypto",
                interval="1m",
                timeout=None
            )   
            d1 = ETHUSDT.get_analysis().summary
            s1 = json.dumps(d1)
            d2 = json.loads(s1)
            RECOMMENDATION = d2['RECOMMENDATION']

            r = requests.get('https://www.binance.com/fapi/v1/ticker/price?symbol=ETHUSDT')
            text = json.loads(r.text)
            
            SYMBOL_NAME = text["symbol"]
            SYMBOL_PRICE = text["price"]
            SYMBOL_TIME_TIMESTAMP = int(text["time"])
            SYMBOL_TIME = datetime.fromtimestamp(SYMBOL_TIME_TIMESTAMP / 1000).strftime("%H:%M:%S")
            SYMBOL_TOTAL = SYMBOL_NAME+ ': ' + SYMBOL_PRICE + '$'
            
            print(f"{SYMBOL_TOTAL} AT {SYMBOL_TIME}")
            print('RECOMMENDATION:', RECOMMENDATION)
            print('-'*63)
            
            last_price.append(SYMBOL_PRICE)
            MAX_PRICE = float(max(last_price))
            MIN_PRICE = float(min(last_price))
            
            print(f'{SYMBOL_NAME} MAX PRICE: {MAX_PRICE}$')
            print(f'{SYMBOL_NAME} MIN PRICE: {MIN_PRICE}$')
            
            PERECENT_DIF = abs(MAX_PRICE - MIN_PRICE) / ((MAX_PRICE + MIN_PRICE) / 2) * 100
            PERECENT_DIF_ROUNDED = round(PERECENT_DIF, 2)
            print(f"{SYMBOL_NAME} PRICE DIFFERENCE BETWEEN {MAX_PRICE}$ & {MIN_PRICE}$ IS - {PERECENT_DIF_ROUNDED}%")
            
            print('-'*63)
            time.sleep(60)
        except Exception as ex:
            print(ex)
        
if __name__ == '__main__':
    main()