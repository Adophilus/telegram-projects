from TelegramProjects.helpers.functions import loadConfig, loadFile, getChats, getMembers
from telethon.tl.types import User

import pytest
from tests.unit.test_001_load_config import test_load_config
from tests.unit.test_002_init_client import test_init_client

@pytest.mark.asyncio
async def test_get_group_or_channel ():
    config = test_load_config()

    client = await test_init_client(config.accounts[0])
    _chats = await getChats(client)
    chats = []
    for chat in _chats:
        if (not isinstance(chat.entity, User)):
            if (chat.entity.participants_count):
                chats.append(chat.entity)
    
    chats = sorted(chats, key=lambda c: c.title)

    print()

    for i in range(len(chats)):
        print(f"{str(i+1).zfill(3)}. {chats[i].title}")
    
    print()
    indx = input("Select a group or channel to fetch its members: ")
    
    members = map(lambda u: u.username, await getMembers(client, chats[int(indx) - 1]))

    print(list(members))

    await client.disconnect()
