import os
import random

from dogehouse import DogeClient
from dogehouse.events import (
    ReadyEvent, RoomsFetchedEvent, RoomJoinEvent,
    MessageEvent, UserJoinEvent, UserLeaveEvent,
)

token = os.getenv("TOKEN", '')
refresh_token = os.getenv("REFRESH_TOKEN", '')

doge = DogeClient(token, refresh_token)

doge._debug_on()


@doge.on_ready
async def make_my_room(event: ReadyEvent) -> None:
    print(f"Successfully connected as @{event.user.username}!")
    await doge.fetch_user(id=event.user.id)

# @doge.on_rooms_fetch
# async def join_any_room(event: RoomsFetchedEvent) -> None:
#     if len(event.rooms) == 0:
#         await doge.create_room("Hello dogehouse.py")
#     else:
#         random_room = random.choice(event.rooms)
#         await doge.join_room(random_room)


# @doge.on_room_join
# async def joined_room(event: RoomJoinEvent) -> None:
#     print("Joined room", event.room.name)


# @doge.on_user_join
# async def greet_user(event: UserJoinEvent) -> None:
#     await doge.send_message(f"Hello @{event.user.username}")
#     await doge.send_message(f"Hi, I sent you a whisper!", whisper_to=[event.user])


# @doge.on_user_leave
# async def user_left(event: UserLeaveEvent) -> None:
#     await doge.send_message(f"Bye @{event.user.username}")


# @doge.on_message
# async def echo_message(event: MessageEvent) -> None:
#     await doge.send_message(f'@{event.message.author.username} said {event.message.content}')


# @doge.command
# async def echo(event: MessageEvent) -> None:
#     msg = event.message
#     await doge.send_message(f'@{msg.author.username} said {msg.content}')


doge.run()
