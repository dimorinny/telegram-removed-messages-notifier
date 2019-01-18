from telethon import TelegramClient, events

from .buffer import CircularBufferDictionary


class MessagesHandler:

    def __init__(
            self,
            messages_buffer_size: int,
            client: TelegramClient
    ):
        self._messages_buffer_size = messages_buffer_size
        self._client = client
        self._me = await self._client.get_me()

    async def handle(self):
        messages_buffer = CircularBufferDictionary(
            limit=self._messages_buffer_size
        )

        @self._client.on(events.NewMessage(incoming=True))
        async def handler_new(event):
            print('Received message: {event}'.format(event=event))

            print('Adding message to buffer...')
            message = event.message
            messages_buffer[message.id] = message
            print('Message with id: {id} added to buffer. Current buffer size: {size}/{capacity}'.format(
                id=message.id,
                size=len(messages_buffer),
                capacity=self._messages_buffer_size
            ))

        @self._client.on(events.MessageDeleted())
        async def handler_deleted(event):
            print(event)
            # await self._client.send_message(self._me.user_id, message)

        try:
            await self._client.run_until_disconnected()
        finally:
            self._client.disconnect()
