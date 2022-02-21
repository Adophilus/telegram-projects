from TelegramProjects.helpers.functions import loadConfig, getClient
import asyncio


async def main():
    config = loadConfig()
    clients = [await getClient(account) for account in config.accounts]

    if all(clients):
        print("Connected clients!")

    for client in clients:
        await client.disconnect()


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
