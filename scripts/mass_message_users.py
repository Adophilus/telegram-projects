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
    "--template", metavar="template", type=str, help="Path to message template"
)
parser.add_argument("--users", metavar="users", type=str, help="Path to users.json")
parser.add_argument(
    "--stats-folder",
    metavar="stats_folder",
    type=str,
    help="Path to store stats folder",
)

args = parser.parse_args()

if not (args.template and args.users and args.stats_folder):
    parser.print_help()
    exit()

messaging_template = loadFile(args.template)
timeout = 60


async def main():
    clients = [await getClient(account) for account in config.accounts]
    stats_file = os.path.join(args.stats_folder, "stats.txt")
    account = 0

    with open(args.users, "r") as fh:
        users = json.load(fh)

    with open(stats_file, "r+") as stats_fh:
        last_user = stats_fh.read()

        for i in range(len(users)):
            user = users[i]
            client = clients[account]

            if last_user:
                if user != last_user:
                    continue

            last_user = user["username"]
            logging.info(f"Sending message to: {user['username']}")

            try:
                await sendMessage(
                    client,
                    user["username"],
                    messaging_template.format(config=config, user=user),
                )
                await client.delete_dialog(user["username"])
                logging.info(f"Sent message to {user['username']} ({i+1}/len(users))")
            except errors.FloodWaitError as e:
                logging.warning(
                    f"FloodWaitError while processing: {user['username']}. Sleeping for {e.seconds}"
                )
                await asyncio.sleep(e.seconds)

            if (i % 10) == 0:
                logging.info(f"Sleeping for {timeout}")
                await asyncio.sleep(timeout)

            stats_fh.seek(0, os.SEEK_SET)
            stats_fh.write(last_user)

            account += 1
            account %= len(config.accounts)

    await client.disconnect()

    logging.info("All done!")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
