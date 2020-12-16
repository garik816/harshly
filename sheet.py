from pprint import pprint

import httplib2
import json
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import telebot

token = 'токен телеграмм бота'
bot = telebot.TeleBot(token)


CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = 'id таблици'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets','v4', http = httpAuth)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    transmitter()
    bot.send_message(message.chat.id, receiver())

def transmitter():
    transmit = service.spreadsheets().values().batchUpdate(
    spreadsheetId = spreadsheet_id,
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "J1:J2",
             "majorDimension": 'ROWS',
             "values": [["=TODAY()"]]}
        ]
    }
    ).execute()

def receiver():
    receiver = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = 'I5:I9',
        majorDimension = 'ROWS'
    ).execute()

    txt = json.dumps(receiver, ensure_ascii=False)
    txt = txt.replace("[\"", "")
    txt = txt.replace("\"]","")
    txt = txt.replace("]}","")
    txt = txt.replace("{\"range\": \"'Лист1'!I5:I9\", \"majorDimension\": \"ROWS\", \"values\": [","")
    return txt

if __name__ == '__main__':
    bot.polling(none_stop=True)
