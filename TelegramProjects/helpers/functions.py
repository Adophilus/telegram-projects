from collections import namedtuple
from telethon.sync import TelegramClient
import json

def loadConfig (config_path = "./.env"):
    with open(config_path, "r") as fh:
        return json.loads(fh.read(), object_hook=lambda d: namedtuple('Config', d.keys())(*d.values()))

def loadFile (file_path):
    with open(file_path, "r") as fh:
        return fh.read()

async def getClient (account):
    client = TelegramClient(account.phone, account.api.id, account.api.hash)
    await client.connect()

    if not (await client.is_user_authorized()):
        await client.send_code_request(account.phone)
        await client.sign_in(account.phone, input("Enter code:"))
    
    return client

async  def sendMessage (client, recepient, message):
    return await client.send_message(recepient, message)

