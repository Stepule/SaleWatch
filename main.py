import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import Product, PriceScraper, PriceRecord, DatabaseHandler

def track_price():
    bitcoin_product = Product(
        name="BITCOIN", 
        url="https://www.kurzy.cz/bitcoin/", 
        shop_name = "Kurzy.cz"
    )

def __repr__(self) -> str:
    return f"Product(name='{self.name}', shop='{self.shop_name}')"
