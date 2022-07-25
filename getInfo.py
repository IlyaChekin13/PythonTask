import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

CREDENTIALS_FILE = "creds.json"
spreadsheet_id = "1JsjoKNWpW_XU5GKpd8S1ZvzwRXOIv8I-uZbuRjPgXng"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets"])

httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range="лист1"
).execute()

data = pd.DataFrame(data=values['values'])
data = data.set_index(0)
new_header = data.iloc[0]
data = data[1:]
data.columns = new_header


    
