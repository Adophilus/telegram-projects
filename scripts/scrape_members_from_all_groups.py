from TelegramProjects.helpers.functions import loadConfig, loadFile, getChats, getClient, getMembers
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from telethon.tl.types import User
from datetime import datetime
from os import mkdir, path
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)
config = loadConfig()

entities = []
res_id = datetime.strftime(datetime.now(), "%Y-%m-%d")

def checkDirs ():
    folder = path.join("res", "groups", res_id)
    if (not path.isdirectory(folder)):
        mkdir(folder)

    folder = path.join("res", "logs", res_id)
    if (not path.isdirectory(folder)):
        mkdir(folder)

async def processEntity (client, entity):
    try:
        _members = await getMembers(client, entity)
        members = []
    except ChatAdminRequiredError:
        logging.warning(f"{entity.title} could not be processed. Reason: not allowed to fetch subscribers")
        return [ False, 0 ]

    checkDirs()
    
    c = 0
    for member in _members:
        if (not member.is_self):
            members.append({
                "id": member.id,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "username": member.username,
                "phone": member.phone
            })
            c += 1

    """
    data = {
        "entity": {
            "id": entity.id,
            "title": entity.title,
            "username": entity.username
        },
        "members": members
    }
    """
    data = members

    file_path = path.join("res", "groups", res_id, f"{entity.id}-{entity.title}.json")

    with open(file_path, "w") as fh:
        json.dump(data, fh)

    return [ True, c ]

async def main ():
    client = await getClient(config.accounts[1])
    
    logging.info("Fetching chats...")
    chats = await getChats(client)

    for chat in chats:
        if (not isinstance(chat.entity, User)):
            if (chat.entity.title != config.channels[0].name):
                logging.info(f"Processing: {chat.entity.title}")

                (status, processed) = await processEntity(client, chat.entity)
                entities.append({
                    "title": chat.entity.title,
                    "participants": {
                        "present": chat.entity.participants_present,
                        "processed": processed
                    }
                })
                
                logging.info(f"Processed: {entity.title}")

    with open(path.join("res", "logs", res_id, "overview_report.json"), "w") as fh:
        json.dump(entities, fh)

    await client.disconnect()

    logging.info("All done!")

loop = asyncio.new_event_loop()
loop.run_until_complete(main())

