from TelegramProjects.helpers.functions import loadConfig, loadFile, getClient, sendMessage
import pytest
from tests.unit.test_001_load_config import test_load_config
from tests.unit.test_002_init_client import test_init_client

@pytest.mark.asyncio
async def test_send_message ():
    config = test_load_config()

    message = loadFile("templates/spreading_awareness.md").format(
        username=config.accounts[1].username,
        formUrl="https://google.com"
    )

    client = await test_init_client(config.accounts[0])
    await sendMessage(client, config.accounts[1].username, message)

    await client.disconnect()
