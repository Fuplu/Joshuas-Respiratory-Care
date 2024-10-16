'''
Miko! Discord bot main file. This file is responsible for starting the bot, and loading all the necessary libraries and files.
Any extra features are referenced by main.py, and are imported as needed. No core functionality is implemented in this file.
'''

import asyncio
import discord
import logging # used for logging messages to the console and log file
import os # used for exiting the program without error messages
import signal # used for handling shutdown signals (ctrl+c)

from discord.ext import commands
from dotenv import load_dotenv # load environment variables from .env file
from dpyConsole import Console # console used for debugging, logging, and shutdown via control panel
from Database.MySQL import connect_pool # connect to the database



###########################################################################################################################



'''
Set up logger and load variables
'''

log_level = os.getenv('LOG_LEVEL')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.WARNING if log_level is None else int(log_level)) # default log level is WARNING
handler = logging.FileHandler(filename='joshua.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)s: %(message)s'))
LOGGER.addHandler(handler)

load_dotenv() # load environment variables from .env file



###########################################################################################################################



'''
Create bot class and define bot intents. These are used to determine what events the bot will receive.
'''
class Bot(commands.Bot):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.all()
        super().__init__(command_prefix='j', intents=intents, case_insensitive=True, help_command=None)
    
    
    
    async def on_ready(self) -> None:
        LOGGER.log(level=logging.INFO, msg=f'Logged in as {client.user} {client.user.id}')
        print('bot online') # for pterodactyl console for online status
        await client.change_presence(activity=discord.Game(name="Fucking your bitch"))

client = Bot()
console = Console(client=client)



###########################################################################################################################



'''
Handle shutdown signal from keyboard and console.
'''

def thread_kill(one=None, two=None):
    print("Shutting down...")
    LOGGER.log(level=logging.CRITICAL, msg="Shutting down...")
    print("Graceful shutdown complete. Goodbye.")
    LOGGER.log(level=logging.CRITICAL, msg="Graceful shutdown complete. Goodbye.")
    os._exit(0)
signal.signal(signal.SIGINT, thread_kill)

@console.command()
async def shutdown(): thread_kill() # pterodactyl panel shutdown command



###########################################################################################################################



'''
Load all cogs from the cogs directories
'''

async def load_cogs_text():
    for filename in os.listdir('./cogs_text'):
        try:
            if filename.endswith('.py'):
                await client.load_extension(f'cogs_text.{filename[:-3]}')
                LOGGER.log(level=logging.DEBUG, msg=f'Loaded text cog: {filename[:-3]}')
        except Exception as e:
            LOGGER.error(f'Failed to load text cog: {filename[:-3]} | {e}')   
    LOGGER.log(level=logging.DEBUG, msg='All text cogs loaded.')

# Cmd cogs only load the 'cog.py' file in each directory
# This is because command cogs are typically more complex
# than text cogs and have a larger backend
async def load_cogs_cmd():
    for dir in os.listdir('./cogs_cmd'):
        for filename in os.listdir(f'./cogs_cmd/{dir}'):
            try:
                if filename != 'cog.py': continue
                await client.load_extension(f'cogs_cmd.{dir}.{filename[:-3]}')
                LOGGER.log(level=logging.DEBUG, msg=f'Loaded cmd cog: {dir}/{filename[:-3]}')
            except Exception as e:
                LOGGER.error(f'Failed to load cmd cog: {filename[:-3]} | {e}')   
    LOGGER.log(level=logging.DEBUG, msg='All cmd cogs loaded.')
    
async def load_cogs_cmd_on_ready():
    for dir in os.listdir('./cogs_cmd_on_ready'):
        for filename in os.listdir(f'./cogs_cmd_on_ready/{dir}'):
            try:
                if filename != 'cog.py': continue
                await client.load_extension(f'cogs_cmd_on_ready.{dir}.{filename[:-3]}')
                LOGGER.log(level=logging.DEBUG, msg=f'Loaded cmd cog on ready: {dir}/{filename[:-3]}')
            except Exception as e:
                LOGGER.error(f'Failed to load cmd cog on ready: {filename[:-3]} | {e}')   
    LOGGER.log(level=logging.DEBUG, msg='All cmd cogs on ready loaded.')

async def load_cogs_console():
    for filename in os.listdir('./cogs_console'):
        try:
            if filename.endswith('.py'):
                console.load_extension(f'cogs_console.{filename[:-3]}')
                LOGGER.log(level=logging.DEBUG, msg=f'Loaded console cog: {filename[:-3]}')
        except Exception as e:
            LOGGER.error(f'Failed to load console cog: {filename[:-3]} | {e}')
    LOGGER.log(level=logging.DEBUG, msg='All console cogs loaded.')



###########################################################################################################################



'''
Start the bot
'''

async def main() -> None:
    async with client:
        await load_cogs_text() # text commands: krm, kd, ...
        await load_cogs_cmd() # /item, /playtime, /play
        console.start()
        await connect_pool() # connect to the database
        # await load_cogs_console() # terminal commands in console (other than shutdown)
        await client.start(os.getenv('DISCORD_TOKEN'))


asyncio.run(main())