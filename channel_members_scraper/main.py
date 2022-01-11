from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient

import asyncio
from datetime import datetime
import json

api_id = 17891922
api_hash = "8485a1ef5bcf67550dc64ca03644725d"
phone = "+2347016719765"
client = TelegramClient(phone, api_id, api_hash)

loop = asyncio.get_event_loop()
groups = []
group_err_count = 0
skip = 1

client.connect()
if not (client.is_user_authorized()):
	client.send_code_request(phone)
	client.sign_in(phone, input("Enter the code: "))

def date_format(message):
	"""
	:param message:
	:return:
	"""
	if type(message) is datetime:
		return message.strftime("%Y-%m-%d %H:%M:%S")
		
async def getGroups ():
	global group_err_count
	chats = await client(GetDialogsRequest(
		offset_date=None,
		offset_id=0,
		offset_peer=InputPeerEmpty(),
		limit=200,
		hash=0))
	chats = chats.chats

	for chat in chats:
		try:
			if (chat.megagroup):
				groups.append(chat)
				print(f"Added {chat.title}")
			else:
				continue
		except Exception as e:
			group_err_count += 1
			print(f"Error occurred while processing chat '{chat.title}'")

async def getGroupsMembers ():
	i = skip
	for group in groups:
		participants = await client.get_participants(group, aggressive=True)
		members = [ participant.to_dict() for participant in participants ]

		with open(f"users-{str(i).zfill(5)}.json", "w") as fh:
			json.dump(members, fh, default=date_format)

		print("All done!")
		print(f"Processed members for {group.title}")
		print()
		i += 1

async def main ():
	await getGroups()

	print(f"Gotten {len(groups)} groups")
	print(f"Had {group_err_count} errors")
	print()
	print()
	print()

	await getGroupsMembers()
	print(f"Gotten {len(members)} users")

loop.run_until_complete(main())