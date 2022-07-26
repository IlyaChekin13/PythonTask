from config import CREDENTIALS_FILE, spreadsheet_id
from getInfo import getData
def main():
    getData(CREDENTIALS_FILE, spreadsheet_id)