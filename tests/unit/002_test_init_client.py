from TelegramProjects.helpers.functions import loadConfig, getClient
import pytest

@pytest.mark.asyncio
async def test_get_client ():
    config = loadConfig()
    await getClient(config.accounts[0])
