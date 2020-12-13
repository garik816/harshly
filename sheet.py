from pprint import pprint

import random
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

random.seed()

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = 'spreadsheet_id'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets','v4', http = httpAuth)


values = service.spreadsheets().values().get(
    spreadsheetId = spreadsheet_id,
    range = 'D3:D',
    majorDimension = 'ROWS'
).execute()
pprint (values)


exit()

