from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getClient,
    sendMessage,
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
    "--account", metavar="account", type=int, help="ID of operating account"
)
parser.add_argument(
    "--template", metavar="path", type=str, help="Path to message template"
)
parser.add_argument("--users", metavar="path", type=str, help="Path to users.json")

args = parser.parse_args()

if not args.template and args.users and args.account:
    parser.print_help()
    exit()

messaging_template = loadFile(args.template)


async def processUser(user):
    user["ref"] = "Bud"
    if user["username"]:
        user["unique"] = user["username"]
        user["ref"] = f"@{user['username']}"
    elif user["phone"]:
        user["unique"] = user["phone"]
    elif user["id"]:
        user["unique"] = user["id"]
    return user


async def main():
    client = await getClient(config.accounts[args.account])

    with open(args.users, "r") as fh:
        users = json.load(fh)

    c = 0
    for user in users:
        await asyncio.sleep(60 * 5)
        user = await processUser(user)
        logging.info(f"Sending message to: {user['unique']}")
        try:
            await sendMessage(
                client,
                user["unique"],
                messaging_template.format(config=config, user=user),
            )
            logging.info(f"Processed user #{c}")
            c += 1
        except Exception as e:
            logging.warning(
                f"Error occurred while sending message to: {user['unique']}. {e}"
            )
    await client.disconnect()

    logging.info("All done!")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
