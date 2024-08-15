import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from tictactoe import tic_tac_toe, init_tictactoe

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_command(tic_tac_toe)

init_tictactoe(bot)

# Run the bot
bot.run(os.getenv('BOT_TOKEN'))
