import requests
from bs4 import BeautifulSoup

def getRate() -> float: 
    rateURL = "http://www.cbr.ru/scripts/XML_daily.asp"
    req = requests.get(rateURL)
    soup = BeautifulSoup(req.text, features='xml')
    USD_to_RUB = soup.find("Valute", {"ID": 'R01235'}).find('Value').text
    
    return float(USD_to_RUB.replace(",", "."))