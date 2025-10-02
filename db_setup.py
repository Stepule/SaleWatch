from models import DatabaseHandler


def setup_database_tables():
    db = DatabaseHandler()
    print ("STATUS")
    print ("Connection to MySQL") 
    if db.connect(): # Vytvoří tabulku pokud neexistuje
        create_prices_table = """
        CREATE TABLE IF NOT EXISTS prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            shop_name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            timestamp DATETIME NOT NULL
        );
        """
        try:
            db.cursor.execute(create_prices_table)
            db.connection.commit()
            print("Database setup complete")
        except Exception as e:
            print (f"Error creating table: {e}")
        finally:
            db.close()
    else:
        print("Setup failed:No connect to MySQL")

setup_database_tables()




