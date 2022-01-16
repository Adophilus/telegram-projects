from src.helpers.classes import RecursiveNamespace
from telethon.sync import TelegramClient
import json

def loadConfig (config_path = "../.env"):
    with open(config_path, "r") as fh:
        return RecursiveNamespace(**json.load(fh))

def getClient (account):
    client = TelegramClient(account.phone, account.api.id, account.api.hash)
    client.connect()

    if not (client.is_user_authorized()):
        client.send_code_request(account.phone)
        client.sign_in(account.phone, input("Enter code:"))

def sendMessage (client, recepient, message):
    client.sendMessage(recepient, message)

