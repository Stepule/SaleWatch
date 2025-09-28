Bitcoin Price Tracker
Jednoduchá Python aplikace navržená pro automatické stahování (scraping) aktuální ceny Bitcoinu (BTC) z webu Kurzy.cz a ukládání historických záznamů do MySQL databáze.
# Vytvoření virtuálního prostředí
python -m venv .venv

# Aktivace (Windows)
.\.venv\Scripts\activate

# Instalace závislostí
pip install mysql-connector-python requests beautifulsoup4
instalace Python 3 a XAMPP (nebo jiný MySQL server)

MySQL:
Aplikace vyžaduje běžící MySQL server a databázi s názvem cena
1.Spusťte modul MySQL v XAMPP Control Panelu.
2.Vytvořte databázi s názvem cena
3.Zkontrolujte soubor models.py a ověřte přihlašovací údaje (defaultně: DB_USER = 'root', DB_PASSWORD = '')
python db_setup.py

Sledování cen: Ten provede jednorázový cyklus: stáhne cenu, uloží ji do databáze a vypíše poslední 2 záznamy.
python main.py



