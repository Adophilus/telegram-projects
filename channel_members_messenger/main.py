from telethon.sync import TelegramClient
import asyncio
import json

api_id = ""
api_hash = ""
phone = ""

client = TelegramClient(phone, api_id, api_hash)
loop = asyncio.get_event_loop()
template_name = "spreading_awareness"

with open("res/users-00001.json", "r") as fh:
	users = json.load(fh)

client.connect()
if not (client.is_user_authorized()):
	client.send_code_request(phone)
	client.sign_in(phone, input("Enter code: "))

async def sendMessage (message, user):
	# TODO: algorithm to send message to user

async def main ():
	with open(f"templates/{template_name}.md", "r") as fh:
		message = fh.read()

	for user in users:
		await sendMessage(message, user)

loop.run_until_complete(main())