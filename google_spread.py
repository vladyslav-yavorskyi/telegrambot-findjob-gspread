import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio


async def getClient():
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    credentials = await ServiceAccountCredentials.from_json_keyfile_name('api_data.json', scope)

    clientS = gspread.authorize(credentials)
    return clientS

# scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('api_data.json', scope)
#
# client = gspread.authorize(credentials)


# sheet = client.open('test_spreadsheet').sheet1.get_all_records()
#
# for item in sheet:
#     print(item)
    # print(f'Zawód:{item.zawód} - opis {item.opis}')