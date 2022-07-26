import requests
from bs4 import BeautifulSoup
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import keyboard


class Task:
    def __init__(self):
        pass
        # Авторизация (можно отдельную функцию) (если нет сохраненной сессии, то попросить логин и пароль)
        # Подлкючение к БД и проверка таблицы (если нет - создать)
        # Выгрузка данных (или снача удалить все из таблицы, а потом выгрузить или выгрузить и сравнить с содержимым таблицы)

    def process(self):
        # Бесконечный цикл (обработать выход из него на нажатие кнопки)
            # Ожидание триггера на изменение
            # Проверка курса доллара
        while True:
            if keyboard.is_pressed('esc'):
                break
        



    def getRate(self) -> float: 
        rateURL = "http://www.cbr.ru/scripts/XML_daily.asp"
        req = requests.get(rateURL)
        soup = BeautifulSoup(req.text, features='xml')
        USD_to_RUB = soup.find("Valute", {"ID": 'R01235'}).find('Value').text

        return float(USD_to_RUB.replace(",", "."))

    def getData(self) -> list:
        CREDENTIALS_FILE = "/Users/ilyac/Dev/web/PythonTask/creds.json"
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
                majorDimension='COLUMNS'
            ).execute()
            data = values['values']
        except Exception as error:
            print("Error while getting the data from google sheet\n", error)
            return -3

        dates = tuple(data[3])
        data[3][0] = 'стоимость руб'
        for i in range(1, len(data[2])):
            data[3][i] = round(float(data[2][i]) * self.getRate(), 2)
        data.append(list(dates))

        return data