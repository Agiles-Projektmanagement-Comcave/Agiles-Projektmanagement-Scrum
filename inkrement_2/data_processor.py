import pandas as pd
import numpy as np
from database import get_session, PriceData
from sqlalchemy import select, func, desc
import ta

class DataProcessor:
    def __init__(self):
        self.session = get_session()

    def get_price_data_in_range(self, start_timestamp, end_timestamp , limit=None):
        if start_timestamp != None and end_timestamp != None:
            query = select(PriceData).where(PriceData.timestamp.between(start_timestamp, end_timestamp))
            if limit:
                query = query.limit(limit)
            return self._get_price_data(query)
        return None
            
    def get_price_data_random(self, limit=1000):
            r_query = select(PriceData).order_by(func.random()).limit(1)
            random_entrie = self.session.execute(r_query).scalars().all()
            df = self.convert_query_records_to_dataframe(random_entrie)

            start_timestamp = '2012-01-01 10:01:00.000000'
            end_timestamp = df.iloc[-1]['timestamp']
            print("Suche: Startzeitpunkt", start_timestamp)
            print("Suche: Endzeitpunkt", end_timestamp)

            query = select(PriceData).where(PriceData.timestamp.between(start_timestamp, end_timestamp))
            query = query.limit(limit)
            return self._get_price_data(query)
    
    def convert_query_records_to_dataframe(self, records):
        df = pd.DataFrame([{
            'timestamp': r.timestamp,
            'open': r.open,
            'high': r.high,
            'low': r.low,
            'close': r.close,
            'volume': r.volume
        } for r in records])
        return df

    def get_price_data_from_limit(self, limit=60):
        query = select(PriceData).order_by(desc(PriceData.timestamp))
        if limit:
            query = query.limit(limit)

        records = self.session.execute(query).scalars().all()
        df = self.convert_query_records_to_dataframe(records)
        # timstamp order invertiert
        start_timestamp = df.iloc[-1]['timestamp']
        end_timestamp = df.iloc[0]['timestamp']
        print("Suche: Startzeitpunkt", start_timestamp)
        print("Suche: Endzeitpunkt", end_timestamp)
        return df

    def _get_price_data(self, query):
        """Lade Preisdaten aus der Datenbank"""             
        records = self.session.execute(query).scalars().all()         
        return self.convert_query_records_to_dataframe(records)

    def calculate_indicators(self, df):
        """Berechne technische Indikatoren"""
        # Stelle sicher, dass genügend Daten vorhanden sind
        if len(df) < 50:
            raise ValueError("Nicht genügend Daten für die Berechnung der Indikatoren")

        # RSI (Relative Strength Index)
        df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()

        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(df['close'])
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        df['bb_low'] = bollinger.bollinger_lband()

        # Moving Averages
        df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(df['close'], window=50).sma_indicator()
        df['sma_200'] = ta.trend.SMAIndicator(df['close'], window=200).sma_indicator()

        # ATR (Average True Range)
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()

        return df

    def analyze_market_conditions(self, df):
        """Analysiere Marktbedingungen basierend auf technischen Indikatoren"""
        latest = df.iloc[-1]
        
        conditions = {
            'trend': {
                'short_term': 'bullish' if latest['close'] > latest['sma_20'] else 'bearish',
                'medium_term': 'bullish' if latest['close'] > latest['sma_50'] else 'bearish',
                'long_term': 'bullish' if latest['close'] > latest['sma_200'] else 'bearish'
            },
            'momentum': {
                'rsi': latest['rsi'],
                'rsi_condition': 'overbought' if latest['rsi'] > 70 else 'oversold' if latest['rsi'] < 30 else 'neutral',
                'macd': 'bullish' if latest['macd'] > latest['macd_signal'] else 'bearish'
            },
            'volatility': {
                'bb_position': 'div zero' if (latest['bb_high'] - latest['bb_low']) == 0 else (latest['close'] - latest['bb_low']) / (latest['bb_high'] - latest['bb_low']),
                'atr': latest['atr']
            }
        }
        
        return conditions

    def generate_signals(self, df):
        """Generiere Trading-Signale basierend auf der technischen Analyse"""
        conditions = self.analyze_market_conditions(df)
        
        # Trading-Signal-Logik
        signal = 'hold'  # Standard: halten
        
        # RSI-basierte Signale
        if conditions['momentum']['rsi'] < 30:  # Überverkauft
            signal = 'buy'
        elif conditions['momentum']['rsi'] > 70:  # Überkauft
            signal = 'sell'
            
        # MACD-Bestätigung
        if signal == 'buy' and conditions['momentum']['macd'] == 'bearish':
            signal = 'hold'  # Kein Kauf ohne MACD-Bestätigung
        elif signal == 'sell' and conditions['momentum']['macd'] == 'bullish':
            signal = 'hold'  # Kein Verkauf ohne MACD-Bestätigung
            
        # Trend-Bestätigung
        if signal == 'buy' and conditions['trend']['medium_term'] == 'bearish':
            signal = 'hold'  # Kein Kauf gegen den mittelfristigen Trend
        elif signal == 'sell' and conditions['trend']['medium_term'] == 'bullish':
            signal = 'hold'  # Kein Verkauf gegen den mittelfristigen Trend
        
        return {
            'signal': signal,
            'conditions': conditions,
            'timestamp': df.iloc[-1]['timestamp']
        }

def test_range_from_to():   
    start_timestamp = '2016-01-31 00:00:00'
    end_timestamp = '2016-01-31 23:59:59'
    print("Test von-bis, letzter gefundener Datensatz wird ausgewertet")
    print("Suche: Startzeitpunkt", start_timestamp)
    print("Suche: Endzeitpunkt", end_timestamp)
    print("Suche im Zeitraum nach dem letzten Eintrag in der Datenbank...")
    return processor.get_price_data_in_range(start_timestamp, end_timestamp)

def test_range_from_to_with_limit(limit):   
    start_timestamp = '2016-01-31 00:00:00'
    end_timestamp = '2016-01-31 23:59:59'
    print("Test von-bis, letzter gefundener Datensatz wird ausgewertet")
    print("Suche: Startzeitpunkt", start_timestamp)
    print("Suche: Endzeitpunkt", end_timestamp)
    print("Suche im Zeitraum nach dem letzten Eintrag in der Datenbank...")
    return processor.get_price_data_in_range(start_timestamp, end_timestamp, limit)

def test_random(limit=1000):
    print("\nEs wird vom frühstmöglichen Eintrag in der Datenbank,\nzu einem zufälligen Eintrag, der letzte Zeitpunkt ausgewertet")
    return processor.get_price_data_random(limit)

def test_from_limit(limit=None):
    print(f"\nVom letzten vorhandenen Datensatz werden, {limit} Einträge vorher bewertet")
    return processor.get_price_data_from_limit(limit)

if __name__ == "__main__":
    processor = DataProcessor()

    #df = test_range_from_to()
    #df = test_range_from_to_with_limit(100)
    #df = test_random(10000)
    df = test_from_limit(60)

    if not df.empty:
        print(f"Anzahl geladener Datenpunkte: {len(df)}")
        
        # Berechne Indikatoren
        print("Berechne technische Indikatoren anhand der Datenpunkte...")
        df_with_indicators = processor.calculate_indicators(df)
        
        # Generiere Trading-Signal
        print("\nGeneriere Trading-Signal zum letzten Zeitpunkt...")
        signal_data = processor.generate_signals(df_with_indicators)
        
        print("\nTrading-Signal:")
        print(f"Zeitpunkt: {signal_data['timestamp']}")
        print(f"Signal: {signal_data['signal'].upper()}")
        print("\nMarktbedingungen:")
        for category, data in signal_data['conditions'].items():
            print(f"\n{category.capitalize()}:")
            for key, value in data.items():
                print(f"{key}: {value}")
    else:
        print("Keine Daten in der Datenbank gefunden.")
