from TelegramProjects.helpers.classes import RecursiveNamespace
from telethon.sync import TelegramClient
import json

def loadConfig (config_path = "./.env"):
    with open(config_path, "r") as fh:
        return RecursiveNamespace(**json.load(fh))

async def getClient (account):
    client = TelegramClient(account.phone, account.api.id, account.api.hash)
    await client.connect()

    if not (await client.is_user_authorized()):
        await client.send_code_request(account.phone)
        await client.sign_in(account.phone, input("Enter code:"))
    
    return client

async def sendMessage (client, recepient, message):
    # if (isinstance(recepient, str)):
    #   recepient = await client.get_entity(recepient)
    await client.send_message(entity=recepient, message=message)

