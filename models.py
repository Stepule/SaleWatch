import mysql.connector
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup


url = 'https://example.com'

#dotaz na web
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

DB_HOST='localhost'
DB_DATABASE='cena'
DB_USER='root'
DB_PASSWORD=" "

# def track_price():
#     bitcoin_product = Product(
#         name="BITCOIN", 
#         url="https://www.kurzy.cz/bitcoin/", 
#         self.shop_name= "Kurzy.cz"
#     )

# def __repr__(self) -> str:
#     return f"Product(name='{self.name}', shop='{self.shop_name}')"


class Product:

    def __init__(self, name: str, url: str, shop_name : str):
        self.name = "BITCOIN"
        self.url = "https://www.kurzy.cz/bitcoin/"
        self.shop_name = "Kurzy.cz"

class PriceRecord:  
    def __init__(self, product: Product, price: float, timestamp: datetime = None):
       self.product = "BITCOIN" 
       self.price = price
       self.timestamp = timestamp if timestamp is not None else datetime.now()

    def __repr__(self) -> str:
        return (f"PriceRecord(product='{self.product.name}', shop='{self.product.shop_name}', "f"price={self.price}, time='{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}')")
# interakce s mysql
class DatabaseHandler:

    def __init__(self, host=DB_HOST, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
#navazani spojeni
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
        except mysql.connection.Error as err:
            print (f"Wrong connection MyQQL: {err}")
            return False
        
   # ukonceni spojeni s databazi
    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    # vlozeni noveho zaznamu
    def save_price(self, price_record: PriceRecord) -> bool:
        if not self.connect():
            return False

        query = """ ... """
        params = (
            price_record.product.name,
            price_record.product.shop_name,
            price_record.price,
            price_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    )
        
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"Saved in DB:  {price_record.product.name} @ {price_record.price}   ")
            return True
        except mysql.connector.Error as err:
            print(f"Something wrong  with saving: {err}")
            return False
        finally:
            self.close()





# stahovani a parsovani ceny z webu
class Pricescraper():

    def __init__(self, product: Product):
     self.product = "BITCOIN"



    def get_price(self) -> float | None:
        print(f" Download prom: {https://www.kurzy.cz/bitcoin/}")

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.product.url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            price_element = soup.select_one('div.cena')

            if price_element:
                price_text = price_element.text
                cleaned_text = price_text.replace('\xa0', '').replace('Kč', '').replace(',', '.').strip()
    #prevod na cislo
                price = float(cleaned_text)
                print(f" Founded price: {price}")
                return price
            else:
                print(f"Wrong: Price not found {self.product.name}")
            return None
        except requests.exceptions.RequestException as e:
            print (f" Wrong parsing:Value '{price_text}' not a number")
            return None 
    