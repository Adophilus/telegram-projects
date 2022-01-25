from TelegramProjects.helpers.functions import loadConfig, loadFile, getChats, getClient, getMembers
from telethon.tl.types import User
from os import path
import asyncio
import json

config = loadConfig()

counter = 0

async def processEntity (client, entity):
    _members = await getMembers(client, entity)
    members = []
    
    print("Processing members...")

    for member in _members:
        if (not member.is_self):
            members.append({
                "id": member.id,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "username": member.username,
                "phone": member.phone
            })

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

    # file_path = path.join("res", "groups", f"group-{str(counter).zfill(4)}.json")
    file_path = path.join("res", "groups", f"{entity.id}-{entity.title}.json")

    print("Saving file...")

    with open(file_path, "w") as fh:
        json.dump(data, fh)

async def main ():
    client = await getClient(config.accounts[1])
    
    print("Fetching chats...")
    chats = await getChats(client)

    for chat in chats:
        if (not isinstance(chat.entity, User)):
            if (chat.entity.title != config.channels[0].name):
                print(f"Processing: {chat.entity.title}")
                await processEntity(client, chat.entity)
                break

    await client.disconnect()

loop = asyncio.new_event_loop()
loop.run_until_complete(main())

