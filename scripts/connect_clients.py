from TelegramProjects.helpers.functions import loadConfig, getClient
import asyncio


async def main():
    config = loadConfig()
    clients = []

    for account in config.accounts:
        try:
            clients.append(await getClient(account))
        except RuntimeError:
            break
        except Exception as e:
            print(f"failed to get client for {account.username}")
            print(e)

    if all(clients):
        print("Connected clients!")

    for client in clients:
        await client.disconnect()


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
