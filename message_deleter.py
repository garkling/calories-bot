from telethon import TelegramClient
from telethon.tl.custom import Message


class MessageDeleter:

    def __init__(self, client: TelegramClient):
        self.bot = client
        self.message_to_delete = dict()

    def add_messages_to_delete(self, user_id,  *message_ids):
        self.message_to_delete[user_id] = message_ids

    def delete_previous_messages(self, f):

        async def wrapper(event: Message):
            user_id = event.sender_id
            message_ids_to_delete = self.message_to_delete.get(user_id, [])
            await f(event)
            await self.bot.delete_messages(user_id, message_ids_to_delete)

        return wrapper
