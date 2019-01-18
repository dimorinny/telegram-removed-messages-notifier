import asyncio

from telethon import TelegramClient

from .handler import MessagesHandler


class Command:

    def __init__(
            self,
            messages_buffer_size: int,
            api_id: int,
            api_hash: str,
            phone_number: str,
            send_stacktrace_to_telegram: bool = True
    ):
        self._messages_buffer_size = int(messages_buffer_size)
        self._api_id = int(api_id)
        self._api_hash = str(api_hash)
        self._phone_number = str(phone_number)
        self._send_stacktrace_to_telegram = bool(send_stacktrace_to_telegram)

    def start(self, session: str):
        asyncio.run(
            self._start(session)
        )

    def make_session(self, session: str):
        asyncio.run(
            self._make_session(session)
        )

    async def _start(self, session: str):
        client = await self._start_client(session)
        me = await client.get_me()

        self._print_params('start', me, session)

        await MessagesHandler(
            messages_buffer_size=self._messages_buffer_size,
            client=client,
            send_stacktrace_to_telegram=self._send_stacktrace_to_telegram
        ).handle()

    async def _make_session(self, session: str):
        client = await self._start_client(session)
        me = await client.get_me()

        self._print_params('make_session', me, session)

    async def _start_client(self, session: str) -> TelegramClient:
        client = TelegramClient(
            session=session,
            api_id=self._api_id,
            api_hash=self._api_hash,
        )

        await client.start(
            phone=self._phone_number
        )

        return client

    def _print_params(self, command: str, me, *args):
        print(
            """
Command: {command}
With arguments: {arguments}

Api id: {api_id}
Api hash: {api_hash}
Phone number: {phone_number}
Buffer size: {buffer_size}
Send stacktrace to telegram: {send_stacktrace_to_telegram}
User info: {user}
            """.format(
                command=command,
                arguments=args,
                api_id=self._api_id,
                api_hash=self._api_hash,
                phone_number=self._phone_number,
                buffer_size=self._messages_buffer_size,
                send_stacktrace_to_telegram=self._send_stacktrace_to_telegram,
                user=me.stringify()
            )
        )
