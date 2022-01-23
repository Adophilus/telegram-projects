from TelegramProjects.helpers.functions import loadConfig, loadFile, getChats, getMembers
from telethon.tl.types import User

import pytest
from tests.unit.test_001_load_config import test_load_config
from tests.unit.test_002_init_client import test_init_client

@pytest.mark.asyncio
async def test_get_chats ():
    config = test_load_config()

    client = await test_init_client(config.accounts[0])
    chats = await getChats(client)
    for chat in chats:
        if (not isinstance(chat.entity, User)):
            if (chat.entity.participants_count):
                members = await getMembers(client, chat.entity)

    await client.disconnect()
