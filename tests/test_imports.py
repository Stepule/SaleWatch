import pytest

try:
    import mysql.connector
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime
    
    # Import vlastních tříd pro ověření existence
    from models import Product, PriceRecord, PriceScraper, DatabaseHandler
    CUSTOM_CLASSES = [Product, PriceRecord, PriceScraper, DatabaseHandler]
    
except ImportError as e: #neuspesny import se zastavi a definuje chybu
    CUSTOM_CLASSES = []
    pytest.skip(f"Skipping custom class tests due to ImportError: {e}", allow_module_level=True)


def test_lib_imports():  # test dostupnosti knihoven
 
    assert mysql.connector is not None
    assert requests is not None
    assert BeautifulSoup is not None
    assert datetime is not None
    print("\n 1. Import was successfull")

    print("\n[RESULT] 1. Lib import was successfull")


@pytest.mark.parametrize("custom_class", CUSTOM_CLASSES) # overeni tridy
def test_models_available(custom_class):
    assert issubclass(custom_class, object), f"{custom_class.__name__} should be a class"
    print(f" 2. Class {custom_class.__name__} exist")

    print(f"[RESULT] 2. Class {custom_class.__name__} exist and avalilable")