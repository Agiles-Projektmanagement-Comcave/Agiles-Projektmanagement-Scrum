import ccxt
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

class DataCollector:
    def __init__(self):
        load_dotenv()
        # https://docs.ccxt.com/#/
        self.exchange = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_SECRET_KEY')
        })

    def fetch_btc_usd_data(self, timeframe='1d', limit=500):
        """
        Holt BTC/USD Kursdaten von Binance
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv('BTC/USDT', timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return None

    def save_to_csv(self, df, filename='btc_usd_data.csv'):
        """
        Speichert die Daten in einer CSV-Datei
        """
        try:
            df.to_csv(filename, index=False)
            print(f"Daten erfolgreich in {filename} gespeichert")
        except Exception as e:
            print(f"Fehler beim Speichern der CSV-Datei: {e}")

if __name__ == "__main__":
    collector = DataCollector()
    data = collector.fetch_btc_usd_data()
    if data is not None:
        collector.save_to_csv(data)
