import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from getExchangeRates import getRate


def getData():
    CREDENTIALS_FILE = "/Users/ilyac/Dev/web/PythonTask/creds.json"
    spreadsheet_id = "1JsjoKNWpW_XU5GKpd8S1ZvzwRXOIv8I-uZbuRjPgXng"

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets"])
    except Exception as error:
        print("Error while getting credentials\n", error)

    try:
        httpAuth = credentials.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    except Exception as error:
       print("Error while gettting connection to the google sheet\n", error)

    try:   
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="лист1",
            majorDimension='COLUMNS'
        ).execute()
        data = values['values']
    except Exception as error:
        print("Error while getting the data from google sheet\n", error)
    dates = tuple(data[3])
    data[3][0] = 'стоимость руб'
    for i in range(1, len(data[2])):
        data[3][i] = float(data[2][i]) * getRate()
    data.append(list(dates))

    return data