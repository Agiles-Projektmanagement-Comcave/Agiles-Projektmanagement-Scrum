# Sprint 2
## Installation
Neue python Bibliothek: ta

Vorausetzungen os: Python 3.10.6, git

1. Projekt von Git clonen
2. .venv erstellen: python -m venv .\.venv   
3. venv aktivieren: .venv/scripts/activate   
4. terminal zeile sollte nun ähnlich wie folgt beginnen: (.venv) usw.
5. pip install pandas==2.1.1
6. pip install requests==2.31.0
7. pip install python-dotenv==1.0.0
8. pip install sqlalchemy==2.0.21
9. pip install ccxt==4.1.13
10. pip install numpy==1.24.3
11. pip install pytest==7.4.2
12. **pip install ta**
12. ausführen von: data_processor.py

### Ziel: Mustererkennungssystem entwickeln

### Sprint Backlog
1. Basis-Algorithmus entwickeln
   + Muster definieren
   + Erkennungslogik implementieren
   + Test-Framework aufsetzen
   + manuelle Tests (data_processor.py)

2. Erste Optimierungen
   + Performance-Verbesserungen
   - Fehlertoleranz erhöhen

### Dailies
- Täglich 15 Minuten
- Zeitpunkt: morgens
- Format: Stand-up Meeting
- Fragen:
  * Was wurde gestern erreicht?
  * Was ist für heute geplant?
  * Gibt es Hindernisse?

# Epic 2: Mustererkennungssystem

3. Als Analyst möchte ich Trading-Muster in den Daten erkennen
   - Priorität: Mittel
   - Akzeptanzkriterien:
     * [erledigt] Algorithmus erkennt definierte Muster = data.processor.py
     * [erledigt] Performance-Metriken implementiert = Trend, Volatilität, Momentum
     * [erledigt] Visualisierung der Ergebnisse = Terminal-Ausgabe