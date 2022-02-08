from tests.unit import test_load_config
from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getChats,
    getClient,
    getMembers,
    sendMessage,
)
from telethon.tl.types import User
import asyncio
import pytest


async def initClient(account):
    client = await getClient(account)
    assert client, f"Couldn't init client for {account.phone}"

    return client


@pytest.mark.asyncio
async def test_initClients():
    config = test_load_config()

    for account in config.accounts:
        client = await initClient(account)
        assert client, f"Failed to initialize client for account {account.phone}"
        await client.disconnect()


@pytest.mark.asyncio
async def test_sendMessage():
    config = test_load_config()
    message = loadFile("templates/test.md").format(
        config=config, username=config.accounts[1].username
    )
    client = await initClient(config.accounts[0])
    await sendMessage(client, config.accounts[1].username, message)

    await client.disconnect()


@pytest.mark.asyncio
async def test_getChats():
    config = test_load_config()
    client = await initClient(config.accounts[1])
    chats = await getChats(client)

    await client.disconnect()


@pytest.mark.asyncio
async def test_getGroupOrChannel():
    config = test_load_config()
    client = await initClient(config.accounts[0])
    chats = sorted(
        filter(
            lambda chat: (
                (not (isinstance(chat.entity, User)) and chat.entity.participants_count)
            ),
            await getChats(client),
        ),
        key=lambda c: c.title,
    )
    members = await getMembers(client, chats[0])

    await client.disconnect()


@pytest.mark.asyncio
async def test_getChats():
    config = test_load_config()

    client = await initClient(config.accounts[0])
    chats = await getChats(client)
    for chat in chats:
        if not isinstance(chat.entity, User):
            if chat.entity.participants_count:
                members = await getMembers(client, chat.entity)

    await client.disconnect()
