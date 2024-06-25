from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import Intents
import asyncio
import os
import logging
from bot.config_loader import config_loader

try:
  class MyBot(commands.Bot):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.gold_cog = None
          self.config_reloader.start()

      @tasks.loop(seconds=10)
      async def config_reloader(self):
          if config_loader.is_config_updated("./config"):
              await config_loader.load_config("config")
          for filename in os.listdir('./bot/cogs'):
              if filename.endswith('.py') and filename != '__init__.py':
                  if config_loader.is_config_updated(filename[:-3]):
                      await config_loader.load_config(filename[:-3])

  async def load():
    intents = Intents.default()
    intents.members = True
    intents.messages = True
    intents.guilds = True
    intents.message_content = True
    bot = MyBot(command_prefix="!", intents=intents, help_command=None, case_insensitive=True)
    for filename in os.listdir('./bot/cogs'):
      if filename.endswith('.py') and filename != '__init__.py':
        print(f'Loading {filename}...')
        await bot.load_extension(f'bot.cogs.{filename[:-3]}')
    return bot


  async def main():
      try:
        bot = await load()
        global_config = await config_loader.load_config("config")
        if global_config and 'bot_token' in global_config:
            print("Starting bot...")
            await bot.start(global_config['bot_token'])
            print(f"Config reloader loop started: {bot.config_reloader.is_running()}")
        else:
            print("Failed to load bot token from config.")
      except Exception as e:
        print(e)

  asyncio.run(main())
except Exception as e:
  print(e)