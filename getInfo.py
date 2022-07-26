import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def getData(creds, sheet_id):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            creds, ["https://www.googleapis.com/auth/spreadsheets"])
    except Exception as error:
        print("Error while getting credentials\n", error)

    try:
        httpAuth = credentials.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
    except Exception as error:
        print("Error while gettting connection to the google sheet\n", error)

    try:   
        values = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range="лист1"
        ).execute()
    except Exception as error:
        print("Error while getting the data from google sheet\n", error)

    data = pd.DataFrame(data=values['values'])
    data = data.set_index(0)
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header

    return data



    
