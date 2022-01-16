from TelegramProjects.helpers.functions import loadConfig, getClient
import pytest
from tests.unit.test_001_load_config import test_load_config

@pytest.mark.skip
@pytest.mark.asyncio
async def test_init_client (account):
    client = await getClient(account)
    assert client, f"Couldn't init client for {account.phone}"

    return client

@pytest.mark.asyncio
async def test_init_clients ():
    config = test_load_config()

    client_1 = await test_init_client(config.accounts[0])
    client_2 = await test_init_client(config.accounts[1])

    await client_1.disconnect()
    await client_2.disconnect()
