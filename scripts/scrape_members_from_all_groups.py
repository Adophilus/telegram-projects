from TelegramProjects.helpers.functions import (
    loadConfig,
    loadFile,
    getChats,
    getClient,
    getMembers,
    handleMultiError,
)
from telethon import errors
from telethon.tl.types import User
from datetime import datetime
from os import mkdir, path
import argparse
import asyncio
import json
import logging
import logging.config

parser = argparse.ArgumentParser(
    description="Scrapes all members from channels and groups account is in"
)
parser.add_argument(
    "--account", metavar="account", type=int, help="ID of operating account"
)

args = parser.parse_args()

if not (args.account):
    parser.print_help()
    exit()

res_id = datetime.strftime(datetime.now(), "%Y-%m-%d")
folder = {}

folder["groups"] = path.join("res", "groups", res_id)
if not path.isdir(folder["groups"]):
    mkdir(folder["groups"])

folder["logs"] = path.join("res", "logs", res_id)
if not path.isdir(folder["logs"]):
    mkdir(folder["logs"])

logging.config.fileConfig(fname=".loggingrc", disable_existing_loggers=False)
config = loadConfig()
entities = []


async def processEntity(client, entity):
    members = []

    async def _():
        return await getMembers(client, entity)

    try:
        _members = await getMembers(client, entity)
    except errors.common.MultiError as e:
        _members = await handleMultiError(e.exceptions, _)
    except errors.FloodWaitError as e:
        _members = await handleMultiError([e], _)
    except errors.rpcerrorlist.ChatAdminRequiredError:
        logging.warning(
            f"{entity.title} could not be processed. Reason: not allowed to fetch subscribers"
        )
        return [False, 0]

    c = 0
    for member in _members:
        if not member.is_self:
            members.append(
                {
                    "id": member.id,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "username": member.username,
                    "phone": member.phone,
                }
            )
            c += 1

    file_path = path.join(folder["groups"], f"{entity.id}-{entity.title}.json")

    with open(file_path, "w") as fh:
        json.dump(members, fh)

    return [True, c]


async def main():
    client = await getClient(config.accounts[args.account])

    logging.info("Fetching chats...")
    chats = await getChats(client)

    for chat in chats:
        if not isinstance(chat.entity, User):
            if chat.entity.title != config.channels[0].name:
                logging.info(f"Processing: {chat.entity.title}")

                (status, processed) = await processEntity(client, chat.entity)
                entities.append(
                    {
                        "title": chat.entity.title,
                        "participants": {
                            "present": chat.entity.participants_count,
                            "processed": processed,
                        },
                    }
                )

                logging.info(f"Processed: {chat.entity.title}")

    with open(path.join(folder["logs"], "overview_report.json"), "w") as fh:
        json.dump(entities, fh)

    await client.disconnect()

    logging.info("All done!")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
