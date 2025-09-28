from datetime import datetime
from models import Product, PriceScraper, PriceRecord, DatabaseHandler

def track_price():
    bitcoin_product = Product(
        name="BITCOIN", 
        url="https://www.kurzy.cz/bitcoin/", 
        shop_name = "Kurzy.cz"
    )
    print(f"Scan: {bitcoin_product.name} ---")

    scraper = PriceScraper(bitcoin_product)
    price = scraper.get_price()

    if price is not None:
        record = PriceRecord(product= bitcoin_product, price=price, timestamp=datetime.now())

        #ulozeni do databaze
        db_handler = DatabaseHandler()
        db_handler.save_price(record)
    else:
        print("Price could not be retrieved")

def check_records():
    db_handler = DatabaseHandler()
    all_prices = db_handler.get_all_records()

    if all_prices:
        print("")
        for record in all_prices[:2]:
            print (f"ID: {record[0]}, Name: {record[1]}, Price: {record[3]}, Time: {record[4]}")
    else:
         print ("Database is empty or failed for it")

  
track_price()
check_records()



