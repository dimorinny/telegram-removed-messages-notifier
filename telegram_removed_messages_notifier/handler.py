import traceback
from copy import copy

from telethon import TelegramClient, events

from .buffer import CircularBufferDictionary


class MessagesHandler:
    TAG = '#resender'

    def __init__(
            self,
            messages_buffer_size: int,
            send_stacktrace_to_telegram: bool,
            client: TelegramClient
    ):
        self._messages_buffer_size = messages_buffer_size
        self._send_stacktrace_to_telegram = send_stacktrace_to_telegram
        self._client = client

    async def handle(self):
        me = await self._client.get_me()
        messages_buffer = CircularBufferDictionary(
            limit=self._messages_buffer_size
        )

        @self._client.on(event=events.NewMessage(incoming=True))
        @self._notify(me=me)
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

        @self._client.on(event=events.MessageDeleted())
        @self._notify(me=me)
        async def handler_deleted(event):
            print('Messages deletion event received: {messages}'.format(
                messages=event
            ))
            for deleted_id in event.deleted_ids:
                if deleted_id in messages_buffer:
                    print('Message with id: {id} found in messages buffer'.format(
                        id=deleted_id
                    ))

                    print('Forwarding message with id: {id}...'.format(
                        id=deleted_id
                    ))
                    await self._resend_message(
                        to=me,
                        message=messages_buffer[deleted_id]
                    )
                    messages_buffer.pop(deleted_id, None)
                    print('Message with id: {id} forwarded'.format(
                        id=deleted_id
                    ))
                else:
                    print('Message with id: {id} not found in message buffer'.format(
                        id=deleted_id
                    ))

        try:
            await self._client.run_until_disconnected()
        finally:
            self._client.disconnect()

    def _notify(self, me):
        def _notify_decorator(function):
            # noinspection PyBroadException
            async def _wrapped(*args, **kwargs):
                try:
                    await function(*args, **kwargs)
                except Exception:
                    stacktrace = traceback.format_exc()
                    print(stacktrace)
                    if self._send_stacktrace_to_telegram:
                        await self._client.send_message(
                            entity=me.id,
                            message='''
{tag}

{stacktrace}
                            '''.format(
                                tag=MessagesHandler.TAG,
                                stacktrace=stacktrace
                            )
                        )

            return _wrapped

        return _notify_decorator

    # noinspection PyBroadException
    async def _resend_message(self, message, to):
        print('Loading user by id: {id}'.format(
            id=message.from_id
        ))
        try:
            user_from = await self._client.get_entity(message.from_id)
        except Exception:
            print(traceback.format_exc())
            print('Something went wrong during loading user with id: {id}'.format(
                id=message.from_id
            ))
            user = str(message.from_id)
        else:
            print('User with id: {id} loaded: {user}'.format(
                id=message.from_id,
                user=user_from
            ))
            user = user_from.username

        modified_message = copy(message)
        modified_message.message = '''
{tag}

{date}: @{user_from}:
{message}
        '''.format(
            tag=MessagesHandler.TAG,
            date=modified_message.date.strftime("%Y-%m-%d %H:%M"),
            user_from=user,
            message=modified_message.message
        )

        await self._client.send_message(
            entity=to.id,
            message=modified_message
        )
