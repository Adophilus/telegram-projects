from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getClient,
    sendMessage,
)
from telethon import errors
from telethon.tl.types import User
from datetime import datetime
from os import mkdir, path
import argparse
import asyncio
import json
import os
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
parser.add_argument(
    "--sessions",
    metavar="sessions",
    type=str,
    help="Path to sessions folder",
)

args = parser.parse_args()

if not (args.template and args.users and args.stats_folder):
    parser.print_help()
    exit()

messaging_template = loadFile(args.template)
timeout = 60


async def main():
    if args.sessions:
        clients = [
            await getClient(account, args.sessions) for account in config.accounts
        ]
    else:
        clients = [await getClient(account) for account in config.accounts]

    stats_file = os.path.join(args.stats_folder, "stats.txt")
    account = 0

    if os.path.isfile(stats_file):
        stats_file_mode = "r+"
    else:
        stats_file_mode = "w+"

    with open(args.users, "r") as fh:
        users = json.load(fh)

    with open(stats_file, stats_file_mode) as stats_fh:
        last_user = stats_fh.read()
        has_skipped = False

        for i in range(len(users)):
            user = users[i]
            client = clients[account]

            if not (has_skipped):
                if last_user:
                    if user == last_user:
                        has_skipped = True
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
                logging.info(f"Sent message to {user['username']} ({i+1}/{len(users)})")
            except errors.FloodWaitError as e:
                logging.warning(
                    f"FloodWaitError while processing: {user['username']}. Sleeping for {e.seconds}"
                )
                await asyncio.sleep(e.seconds)

            if (i % 24) == 0:
                logging.info(f"Periodic Sleeping for {timeout}")
                await asyncio.sleep(timeout)

            stats_fh.seek(0, os.SEEK_SET)
            stats_fh.write(last_user)

            account += 1
            account %= len(config.accounts)

    for client in clients:
        await client.disconnect()

    logging.info("All done!")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())