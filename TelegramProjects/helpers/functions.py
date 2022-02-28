from collections import namedtuple
from telethon.sync import TelegramClient
import asyncio
import json
from telethon import errors


def loadConfig(config_path="./.env"):
    with open(config_path, "r") as fh:
        return json.loads(
            fh.read(), object_hook=lambda d: namedtuple("Config", d.keys())(*d.values())
        )


def loadFile(file_path):
    with open(file_path, "r") as fh:
        return fh.read()


async def getClient(account):
    client = TelegramClient(account.phone, account.api.id, account.api.hash)
    await client.connect()

    if not (await client.is_user_authorized()):
        await client.send_code_request(account.phone)
        await client.sign_in(
            account.phone, input(f"Enter code for {account.username}: ")
        )

    return client


async def getChats(client):
    return await client.get_dialogs()


async def getMembers(client, group):
    return await client.get_participants(group, aggressive=True)


async def sendMessage(client, recepient, message):
    recepient = await client.get_input_entity(peer=recepient)
    return await client.send_message(entity=recepient, message=message)


async def handleMultiError(_errors, _callback):
    _errors = filter(None, _errors)
    _sleep_timeout = 0
    for _error in _errors:
        if isinstance(_error, errors.FloodWaitError):
            if _error.seconds > _sleep_timeout:
                _sleep_timeout = _error.seconds
    await asyncio.sleep(_sleep_timeout)
    try:
        return await _callback()
    except errors.common.MultiError as e:
        return await handleMultiError(e.exceptions, _callback)
    except errors.FloodWaitError as e:
        return await handleMultiError([e], _callback)
