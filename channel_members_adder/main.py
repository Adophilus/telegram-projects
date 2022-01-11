from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputUser

import asyncio
import json

api_id = "18401108"
api_hash = "4a9e950b0227c386d516302afdaee521"
phone = "+2347039324356"
channel_name = input("Enter channel name: ")

client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not (client.is_user_authorized()):
	client.send_code_request(phone)
	client.sign_in(phone, input("Enter the code: "))

with open("res/SolCharactersAirdropUsers.json", "r") as fh:
	user_ids = json.load(fh)

users = []
channel = None
last_user = None

async def init_channel ():
	global channel
	chann = await client.get_entity(channel_name)
	channel = InputPeerChannel(chann.id, chann.access_hash)

async def init_users ():
	for user_id in user_ids:
		try:
			user = await client(ResolveUsernameRequest(user_id))
			user = InputUser(user.users[0].id, user.users[0].access_hash,)
			users.append(user)
		except Exception as e:
			print(f"Exception occurred while processing user id '{user_id}'")

async def main ():
	print(f"Initializing channel: '{channel_name}'...")
	await init_channel()

	print("Initializing users...")
	await init_users()

	print(f"Adding users to channel: '{channel_name}'...")
	await client(InviteToChannelRequest(channel, users))

	print("All done!")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
