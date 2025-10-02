import pytest
from unittest.mock import MagicMock
from models import Product, PriceScraper 
import requests 


@pytest.fixture
def clean_product():
    return Product(name="TEST_TOKEN", url="http://mock.url/test", shop_name="MockShop")

@pytest.fixture
def scraper_instance(clean_product):
    return PriceScraper(clean_product)

@pytest.fixture
def mock_response(mocker):

    mock_resp = mocker.Mock() # http 200
    mock_resp.raise_for_status = MagicMock() 
    mocker.patch('models.requests.get', return_value=mock_resp)
    return mock_resp


@pytest.mark.parametrize("html_content, expected_price", [
    # Success path
    ("""<html><body><span id="last_czk">1 234 567,89 CZK</span></body></html>""", 1234567.89),
    # Alternative format, dot separator
    ("""<html><body><span id="last_czk">543.210,00</span></body></html>""", 543210.00),
    # Basic price format
    ("""<html><body><span id="last_czk">100,50</span></body></html>""", 100.50),
])
def test_scraper_parsing_success(scraper_instance, mock_response, html_content, expected_price): # test uspesneho stazeni a parsovani ceny

    mock_response.text = html_content # textova odpoved pro mock
    
    price = scraper_instance.get_price()
    
    assert price == expected_price
    print(f"\n Parsing successful: HTML -> Cena {expected_price}")


def test_scraper_price_not_found(scraper_instance, mock_response): # spravne html, ale spatne id
   
    mock_response.text = """<html><body><span id="wrong_id">123.45</span></body></html>"""
    
    price = scraper_instance.get_price()
    
    # Očekáváme None, protože selector #last_czk nebyl nalezen
    assert price is None
    print("\n Price not found; None returned")


def test_scraper_http_request_error(scraper_instance, mocker): # nastala chyba HTTP 404, Timeout
  
    # mock requests.get při volání vyhodí výjimku
    mocker.patch('models.requests.get', side_effect=requests.exceptions.RequestException("Mock HTTP Error"))
    
    price = scraper_instance.get_price()
    
    # Chyba stahovani, vypise se None 
    assert price is None
    print("\n Returned None when HTTP request failed")

def test_scraper_value_error(scraper_instance, mock_response): #ValueError, hodnota kterou nasel se neda prevest na cislo
  
    mock_response.text = """<html><body><span id="last_czk"></span></body></html>"""
    
    price = scraper_instance.get_price()
    
    # spatny prevod
    assert price is None
    print("\n Returned None on failed number conversion")


