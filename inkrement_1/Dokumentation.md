### Ziel: Grundlegende Dateninfrastruktur aufbauen
# Sprint 1: EPIC: 1. Datenerfassung und -speicherung 

## Installation
Vorausetzungen os: Python 3.10.6, git


1. csv von kaggle herunterladen
2. .venv erstellen: python -m venv .\.venv   
3. venv aktivieren: .venv/scripts/activate 
4. **pip install kaggle** 


danach im Terminal zum Download: **kaggle datasets download -d mczielinski/bitcoin-historical-data**


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
12. ausführen von: load_database.py

Datenbank, crypto_data.db, sollte nun mit den Daten der csv befüllt worden sein.

### Epic 1: Datenerfassung und -speicherung
1. Als Entwickler möchte ich CSV-Daten von BTC/Dollar-Kursen abrufen können
   - Priorität: Hoch
   - Akzeptanzkriterien:
     * [**ungetestet**, data_collector.py] API-Verbindung funktioniert
     * [**erledigt**, load_database.py] CSV import funktioniert
     * [**erledigt**, database.py] Daten werden im korrekten Format empfangen
     * [**erledigt**], Fehlerbehandlung implementiert

2. Als Entwickler möchte ich die Daten in einer Datenbank speichern
   - Priorität: Hoch
   - Akzeptanzkriterien:
     * [**erledigt**, database.py] Datenbankschema erstellt
     * [**teilweise**, load_database.py] CRUD-Operationen(create,read,update,delete) implementiert
     * [**erledigt**, gebatchter, transaktioneller db import] Datenintegrität gewährleistet

    