import requests
from bs4 import BeautifulSoup
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import keyboard
import os
import time 


class Task:
    def __init__(self):
        
        # Авторизация (можно отдельную функцию) (если нет сохраненной сессии, то попросить логин и пароль)
        # Подлкючение к БД и проверка таблицы (если нет - создать)
        # Выгрузка данных (или снача удалить все из таблицы, а потом выгрузить или выгрузить и сравнить с содержимым таблицы)
        self.process()

    def process(self):
        """Main process of the app"""
        # Бесконечный цикл (обработать выход из него на нажатие кнопки)
            # Ожидание триггера на изменение
            # Проверка курса доллара
        creds = False
        while True:
            if keyboard.is_pressed('esc'):
                break
            if not creds:
                ExchangeRate = self.getRate()
                creds = self._get_credential_file()
                data = self.getData(creds, ExchangeRate)
                
            
            time.sleep(15)
            ExchangeRate = self.getRate()
            newdata = self.getData(creds, ExchangeRate)
            #checking updates
            if data != newdata:
                if len(data) >= len(newdata):
                    #number of deleted rows
                    deletedRows = len(data) - len(newdata)
                    for i in range(len(data)):
                        if data[i] != newdata[i]:
                            print("{} to {}".format(data[i], newdata[i]))
                            #i row was changed
                            pass
                else:
                    #data of new rows
                    newrows = newdata[len(data):]
                    for i in range(len(newdata)):
                        if data[i] != newdata[i]:
                            #i row was changed
                            pass
            
            data = newdata


    def getRate(self) -> float: 
        rateURL = "http://www.cbr.ru/scripts/XML_daily.asp"
        req = requests.get(rateURL)
        soup = BeautifulSoup(req.text, features='xml')
        USD_to_RUB = soup.find("Valute", {"ID": 'R01235'}).find('Value').text

        return float(USD_to_RUB.replace(",", "."))

    def getData(self, creds, Rate) -> list:
        CREDENTIALS_FILE = creds
        #CREDENTIALS_FILE = "/Users/ilyac/Dev/web/creds.json"
        spreadsheet_id = "1JsjoKNWpW_XU5GKpd8S1ZvzwRXOIv8I-uZbuRjPgXng"
    
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets"])
        except Exception as error:
            print("Error while getting credentials\n", error)
            return -1
        
        try:
            httpAuth = credentials.authorize(httplib2.Http())
            service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
        except Exception as error:
           print("Error while gettting connection to the google sheet\n", error)
           return -2

        try:   
            values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range="лист1",
                majorDimension='ROWS'
            ).execute()
            data = values['values']
        except Exception as error:
            print("Error while getting the data from google sheet\n", error)
            return -3
        
        data[0].append('срок поставки')
        data[0][3] = "стоимость руб"
        for i in range(1, len(data)):
            data[i].append(data[i][3])
            data[i][3] = round(float(data[i][2]) * Rate, 2)

        return data

    def _get_credential_file(self) -> str:
        """Gets the json file with credentials"""

        CREDENTIALS_FILE = input('Write path to your credentials json file:\n')
        if os.path.isfile(CREDENTIALS_FILE):
            return(str(CREDENTIALS_FILE))
        else:
            print("Wrong path! \nTry again.")
            self._get_credential_file()



a = Task()
a.process()