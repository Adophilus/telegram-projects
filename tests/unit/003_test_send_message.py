from TelegramProjects.helpers.functions import loadConfig, getClient, sendMessage
import pytest

@pytest.mark.asyncio
async def test_send_message ():
    config = loadConfig()
    client = await getClient(config.accounts[0])
    # await sendMessage(client, "@Echooechobot", "Hello there")
    await sendMessage(client, "@MaryBright1", "Hello there")
