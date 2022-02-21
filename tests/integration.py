from tests.unit import test_load_config as loadConfig
from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getChats,
    getClient,
    getMembers,
    handleMultiError,
    sendMessage,
)
from telethon.tl.types import User
from telethon import errors
import asyncio
import pytest


async def initClient(account):
    client = await getClient(account)
    assert client, f"Couldn't init client for {account.phone}"

    return client


@pytest.mark.skip
@pytest.mark.asyncio
async def test_initClients():
    config = loadConfig()

    for account in config.accounts:
        client = await initClient(account)
        assert client, f"Failed to initialize client for account {account.phone}"
        await client.disconnect()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_sendMessage():
    config = loadConfig()
    message = loadFile("templates/test.md").format(
        config=config, username=config.accounts[1].username
    )
    client = await initClient(config.accounts[0])
    await sendMessage(client, config.accounts[1].username, message)

    await client.disconnect()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_getChats():
    config = loadConfig()
    client = await initClient(config.accounts[1])
    chats = await getChats(client)

    await client.disconnect()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_getGroupOrChannel():
    config = loadConfig()
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

    async def _():
        return await getMembers(client, chats[0])

    try:
        members = await getMembers(client, chats[0])
    except errors.common.MultiError as e:
        members = await handleMultiError(e.exceptions, _)
    except errors.FloodWaitError as e:
        members = await handleMultiError([e], _)

    await client.disconnect()


@pytest.mark.asyncio
async def test_getChats():
    config = loadConfig()
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

    c = 0
    members = []

    async def _():
        return [await getMembers(client, chat) for chat in chats[c:]]

    try:
        for i in range(len(chats)):
            members.append(await getMembers(client, chats[i]))
            c = i
    except errors.common.MultiError as e:
        await handleMultiError(e.exceptions, _)
    except errors.FloodWaitError as e:
        await handleMultiError([e], _)

    print(members)

    await client.disconnect()
