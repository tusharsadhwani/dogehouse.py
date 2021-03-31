# -*- coding: utf-8 -*-
# MIT License

# Copyright (c) 2021 Arthur

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .utils.representation import Represents as Repr
from .utils.parsers import parse_tokens_to_message as parse_tokens
from .utils.convertors import Convertor

from datetime import datetime
from dateutil.parser import isoparse
from typing import List, Dict, List, Union


class BaseUser(Convertor, Repr):
    def __init__(self, id: str, username: str, displayname: str, avatar_url: str):
        """
        Represents the most basic information of a fetched user.

        Args:
            id (str): The user their id.
            username (str): The username of the user. (Their mention name)
            displayname (str): The displayname of the user.
            avatar_url (str): The user their avatar URL.
        """
        self.id: str = id
        self.username: str = username
        self.displayname: str = displayname
        self.avatar_url: str = avatar_url
        self.mention: str = f"@{username}"

    def __str__(self):
        return self.username

    @staticmethod
    def from_dict(data: dict):
        """
        Parses a BaseUser object from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            BaseUser: A parsed BaseUser object which contains the data from the dictionary.
        """
        return BaseUser(data.get("userId"), data.get("username"), data.get("displayName"), data.get("avatarUrl"))

    @classmethod
    async def convert(cls, ctx, param, argument: str):
        return (await cls._get_user(cls.__name__, ctx.client, param, argument)).to_base_user()


class Permission(Repr):
    def __init__(self, asked_to_speak: bool, is_mod: bool, is_admin: bool):
        """
        Represents a user their permissions

        Args:
            asked_to_speak (bool): Whether or not the user has requested to speak.
            is_mod (bool): Wheter or not the user is a room moderator.
            is_admin (bool): Wheter or not the user is a room admin.
        """
        self.asked_to_speak: bool = asked_to_speak
        self.is_mod: bool = is_mod
        self.is_admin: bool = is_admin
        
    @staticmethod
    def from_dict(data: dict):
        """
        Parses permissions from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            Permission: A parsed Permission object which contains the data from the dictionary.
        """
        if data:
            return Permission(data.get("askedToSpeak"), data.get("isMod"), data.get("isAdmin"))
        return Permission(False, False, False)


class User(BaseUser, Repr):
    def __init__(self, id: str, username: str, displayname: str, avatar_url: str, bio: str, last_seen: str, online: bool,
                 following: bool, room_permissions: Permission, num_followers: int, num_following: int, follows_me: bool, current_room_id: str):
        """
        Represents a dogehouse.tv user.

        Args:
            id (str): The user their id.
            username (str): The username of the user. (Their mention name)
            displayname (str): The displayname of the user.
            avatar_url (str): The user their avatar URL.
            bio (str): The user ther biography.
            last_seen (str): When the user was last online.
            online (bool): Whether or not the user is currently online
            following (bool): Wheter or not the client is following this user.
            room_permissions (Permission): The user their permissions for the current room.
            num_followers (int): The amount of followers the user has.
            num_following (int): The amount of users this user is following.
            follows_me (bool): Wether or not the user follows the client.
            current_room_id (str): The user their current room id.
        """
        super().__init__(id, username, displayname, avatar_url)
        self.bio: str = bio
        self.last_seen: datetime = isoparse(last_seen)
        self.online: bool = online
        self.following: bool = following
        self.room_permissions: Permission = room_permissions
        self.num_followers: int = num_followers
        self.num_following: int = num_following
        self.follows_me: bool = follows_me
        self.current_room_id: str = current_room_id

    def __str__(self):
        return self.username

    @staticmethod
    def from_dict(data: dict):
        """
        Parses a User object from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            User: A parsed User object which contains the data from the dictionary.
        """
        return User(data.get("id"), data.get("username"), data.get("displayName"), data.get("avatarUrl"), data.get("bio"), data.get("lastOnline"),
                    data.get("online"), data.get("youAreFollowing"), Permission.from_dict(data.get("roomPermissions")), data.get("numFollowers"), 
                    data.get("numFollowing"), data.get("followsYou"), data.get("currentRoomId"))

    def to_base_user(self) -> BaseUser:
        """
        Convert a user object to a base user object.
        This is intended for internal use (Convertors), as you can access all baseuser properties from the user object.

        Returns:
            BaseUser: The newly created baseuser object, which is derived from the current object.
        """
        return BaseUser(self.id, self.username, self.displayname, self.avatar_url)

    @classmethod
    async def convert(cls, ctx, param, argument: str):
        return await cls._get_user(cls.__name__, ctx.client, param, argument)


class UserPreview(Convertor, Repr):
    def __init__(self, id: str, displayname: str, num_followers: int):
        """
        Represents a userpreview from the Client.rooms users list.

        Args:
            id (string): The user their id.
            displayname (string): The display name of the user.
            num_followers (integer): The amount of followers the user has.
        """
        self.id: str = id
        self.displayname: str = displayname
        self.num_followers: int = num_followers

    def __str__(self):
        return self.displayname

    @staticmethod
    def from_dict(data: dict):
        """
        Parses a UserPreview object from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            UserPreview: A parsed userpreview object which contains the data from the dictionary.
        """
        return UserPreview(data["id"], data["displayName"], data["numFollowers"])

    @classmethod
    async def convert(cls, ctx, param, argument: str):
        user = await cls._get_user(cls.__name__, ctx.client, param, argument)
        return UserPreview(user.id, user.displayname, user.num_followers)


class Room(Repr):
    def __init__(self, id: str, creator_id: str, name: str, description: str, created_at: str, is_private: bool, count: int, users: List[Union[User, UserPreview]]):
        """
        Represents a dogehouse.tv room.

        Args:
            id (str): The id of the room.
            creator_id (str): The id of the user who created the room.
            name (str): The name of the room.
            description (str): The description of the room.
            created_at (str): When the room was created.
            is_private (bool): Wheter or not the room is a private or public room
            count (int): The amount of users the room has.
            users (List[Union[User, UserPreview]]): A list of users whom reside in this room.
        """
        self.id: str = id
        self.creator_id: str = creator_id
        self.name: str = name
        self.description: str = description
        self.created_at: datetime = isoparse(created_at)
        self.is_private: bool = is_private
        self.count: int = count
        self.users: List[Union[User, UserPreview]] = users

    def __str__(self):
        return self.name
    
    def __sizeof__(self):
        return self.count

    @staticmethod
    def from_dict(data: dict):
        """
        Parses a Room object from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            Room: A parsed room object which contains the data from the dictionary.
        """
        return Room(data["id"], data["creatorId"], data["name"], data["description"], data["inserted_at"], data["isPrivate"], data["numPeopleInside"],
                    list(map(UserPreview.from_dict, data["peoplePreviewList"])))


class Message(Repr):
    def __init__(self, id: str, tokens: List[Dict[str, str]], is_wisper: bool, created_at: str, author: BaseUser):
        """
        Represents a message that gets sent in the chat.

        Args:
            id (str): The message its id
            tokens (List[Dict[str, str]]): The message content tokens, for if you want to manually parse the message.
            is_wisper (bool): Whether or not the message was whispered to the client.
            created_at (str): When the message was created.
            author (BaseUser): The user who sent the message
        """
        self.id = id
        self.tokens = tokens
        self.is_wisper = is_wisper
        self.created_at = isoparse(created_at)
        self.author = author
        self.content = parse_tokens(tokens)

    def __str__(self):
        return self.content

    @staticmethod
    def from_dict(data: dict):
        """
        Parses a Message object from a dictionary.

        Args:
            data (dict): The parsed json websocket response.

        Returns:
            Message: A parsed message object which contains the data from the dictionary.
        """
        return Message(data["id"], data["tokens"], data["isWhisper"], data["sentAt"], BaseUser.from_dict(data))


class Client(Repr):
    def __init__(self, user: User, room: Room, rooms: List[Room], prefix: List[str]):
        """
        The base client for the DogeHouse client.

        Args:
            user (User): The client its user object.
            room (Room): The current room in wich the Client resides. Is `None` if no room has been joined.
            rooms (List[Room]): A collection of all the rooms which the client has cached. This gets fetched automatically if no room has been joined. You can also update this using the `async DogeClient.get_top_public_rooms` method.
            prefix (List[str]): A collection of prefixes to which the client should respond.
        """
        self.user: User = None
        self.room: Room = room
        self.rooms: List[Room] = rooms
        self.prefix: List[str] = prefix


class Context(Repr):
    def __init__(self, client: Client, message: Message):
        """
        Represents a message its context.

        Args:
            client (Client): The current client.
            message (Message): The message that was sent.
        """
        self.client: Client = client
        self.bot: Client = self.client
        self.message: Message = message
        self.author: BaseUser = message.author
