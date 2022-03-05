from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getClient,
    sendMessage,
    sendMedia,
)
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from telethon.tl.types import User
from datetime import datetime
from os import mkdir, path
import argparse
import asyncio
import json
import logging
import logging.config

config = loadConfig()
logging.config.fileConfig(fname=".loggingrc", disable_existing_loggers=False)

parser = argparse.ArgumentParser(description="Sends messages to user")
parser.add_argument(
    "--account", metavar="account", type=str, help="username of operating account"
)
parser.add_argument("--media", metavar="media", type=str, help="Path to media file")
parser.add_argument("--users", metavar="users", type=str, help="Path to users.json")

args = parser.parse_args()

if not (args.account and args.media and args.users):
    parser.print_help()
    exit()


async def main():
    client = None

    for account in config.accounts:
        if account.username == args.account:
            client = await getClient(account)

    if not (client):
        print("Invalid account!")
        exit()

    with open(args.users, "r") as fh:
        users = json.load(fh)

    for user in users:
        logging.info(f"Sending message to: {user['username']}")
        try:
            await sendMedia(client, user["username"], args.media)
            await client.delete_dialog(user["username"])
        except Exception as e:
            logging.warning(
                f"Error occurred while sending media to: {user['username']}. {e}"
            )

    await client.disconnect()

    logging.info("All done!")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
