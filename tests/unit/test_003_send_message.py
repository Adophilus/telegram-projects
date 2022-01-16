from TelegramProjects.helpers.functions import loadConfig, getClient, sendMessage
import pytest
from tests.unit.test_001_load_config import test_load_config
from tests.unit.test_002_init_client import test_init_client

@pytest.mark.asyncio
async def test_send_message ():
    config = test_load_config()

    client = await test_init_client(config.accounts[0])
    await sendMessage(client, config.accounts[1].phone, "hello")

    await client.disconnect()
