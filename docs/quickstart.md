# Getting started

This page gives a brief introduction to the librayr. It assumes that you have the library installed. If you don't check the [Installing](http://localhost:3000/#/intro?id=installing) portion.

## A minimal bot

Lets make a bot that responds to a specific message and walk you through it.

```py
import dogehouse

class Client(dogehouse.DogeClient):
    @dogehouse.event
    async def on_ready(self):
        print(f"Logged on as {self.user.username}")
        await self.create_room("Hello World")

    @dogehouse.event
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith(".hello"):
            await self.send("Hello!")

Client("token", "access_token").run()
```

Lets name this file `example_bot.py`.

There is already a lot going on here, so lets walk you through it step by step:
1. The first line just imports the library, if a `ModuleNotFoundError` or `ImportError` occus, then head over to the [Installing](http://localhost:3000/#/intro?id=installing) section to properly install the library.
2. Next we create a class and let it inherit the `DogeClient` class. This is required as the `DogeClient` handles the whole library.
3. When we use the `dogehouse.event` decorator we register an event. You can see the events as a callback.  
A callback is a function/method which gets called when something happens. So in the example the `on_ready()` method is called when the client has established a connection and the `on_message()` method gets called when our client has received a message.
4. When our client has successfully established a connection we want to create a room, creating a room automatically results in your client being moved to that room.
5. Since the `on_message()` event gets triggered when any message gets received, it also gets triggered when its own messages get sent. That is why we check if the message author id is the same as our client its idm and if it is we stop the current event call.
6. Afterwards we check if the message its content (so the sentence/word) starts with `.hello`, if it is we send `Hello!` in the room.
7. Finally we run the bot with our `token` and `access_token`, if you need help getting your tokens, look in the [Getting your tokens]() section.

Now that we have made a bot, we still have to run the bot. Because we are using Python this is extremely easy, so we can run it directly using one of these two commands.

```bash
# For unix based systems
$ python3 example_bot.py
# For windows
$ py -3 example_bot.py
```

### Working with the command decorator

Great! You have created your first dogehouse bot! But creating commands this way will eventually get irritating and unmanagable. Thats why we created `command`'s, using almost the same syntax as discord.py for creating commands. Lets take our example and update it so that we have commands using the `command` decorator.

```py
import dogehouse

class Client(dogehouse.DogeClient):
    @dogehouse.event
    async def on_ready(self):
        print(f"Logged on as {self.user.username}")
        await self.create_room("Hello World")

    @dogehouse.command
    async def hello(self, ctx):
        await self.send("Hello!")

Client("token", "access_token", prefix=".").run()
```

Lets walk you through what changed.

1. We created a command using the command decorator. The call for the command is the same as the name of the method.
2. We added a new parameter in the client which specifies a prefix. Since the default prefix is `!` but we want `.`, we have to override this. If you want to use `!` as prefix you don't even need to specify it.

And voilla, you have your command. When making more advanced bots command decorators will be your best friend, as these pre-process everything for you.