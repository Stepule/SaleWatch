import mysql.connector
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Konfigurace databáze
DB_HOST='localhost'
DB_DATABASE='cena'
DB_USER='root'
DB_PASSWORD=''

# Product
class Product:

    def __init__(self, name: str, url: str, shop_name : str):
        self.name = "BITCOIN"
        self.url = "https://www.kurzy.cz/bitcoin/"
        self.shop_name = "Kurzy.cz"

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', shop='{self.shop_name}')"

# 2 PriceRecord
class PriceRecord: # ukládání záznamů v čase

    def __init__(self, product: Product, price: float, timestamp: datetime = None):
        self.product = product 
        self.price = price
        self.timestamp = timestamp if timestamp is not None else datetime.now()

    def __repr__(self) -> str:
        return (f"PriceRecord(product='{self.product.name}', shop='{self.product.shop_name}', "
                f"price={self.price}, time='{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}')")


# PriceScraper
class PriceScraper: #
    
    def __init__(self, product: Product):
        self.product = product
#http get požadavek na url, který je uložená v self.product.url
    def get_price(self) -> float | None:
        print(f"Downloading data from: {self.product.url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.product.url, headers=headers, timeout=15)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')

            price_element = soup.select_one('#last_czk') 

            if price_element:
                price_text = price_element.text
                cleaned_text = price_text.replace('\xa0', '').replace('CZK', '').replace(',', '.').strip()
                price = float(cleaned_text) # prevedeni na cislo
                print(f"Price found: {price}")
                return price
            else:
                print(f"Error: Price not found for {self.product.name}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"Error during downloading: {e}")
            return None
        except ValueError:
            print(f"Parsing error: The found value is not a number")
            return None

# DatabaseHandler
class DatabaseHandler: #mysql komunikace

    def __init__(self, host=DB_HOST, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}. Check MySQK server.")
            return False

    def close(self): # ukoncení komunikace s databází

        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def save_price(self, price_record: PriceRecord) -> bool: # vlozi novi zaznam do tabulky
        if not self.connect():
            return False
        query = """
        INSERT INTO prices (product_name, shop_name, price, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        params = (
            price_record.product.name,
            price_record.product.shop_name,
            price_record.price,
            price_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"Saved to DB: {price_record.product.name} @ {price_record.price}")
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            return False
        finally:
            self.close()

    def get_all_records(self): # vraceni zaznamu pro overeni
        if not self.connect():
            return None
        
        try:
            self.cursor.execute("SELECT * FROM prices ORDER BY timestamp DESC")
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.close()
