import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
from server import run_dummy_server
from tictactoe import tic_tac_toe, init_tictactoe
from gif import gif, init_gifs, fetch_gifs
from quote import quote, init_quote, fetch_quote_of_day, fetch_verse_of_day
from remind import remind, init_remind
from message_handler import handle_message
#from tiktok import tiktok_all, tiktok_55, tiktok_gedipliusas, init_tiktok_tokens, get_tiktok_videos

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.add_command(tic_tac_toe)
bot.add_command(gif)
bot.add_command(quote)
bot.add_command(remind)
#bot.add_command(tiktok_all)
#bot.add_command(tiktok_55)
#bot.add_command(tiktok_gedipliusas)

init_tictactoe(bot)
#init_quote(os.getenv("QUOTE_API_KEY"), os.getenv("BIBLE_API_KEY"))
init_gifs(bot, int(os.getenv("GIF_CHANNEL_ID")))
init_remind(bot)
#init_tiktok_tokens(os.getenv("TIKTOK_TOKENS").split(","))

@bot.event
async def on_ready():
    print("Bot is ready.")
    fetch_gifs.start()
    #get_tiktok_videos.start()
    #fetch_quote_of_day.start()
    #fetch_verse_of_day.start()

@bot.event
async def on_message(message):
    await handle_message(bot, message)

t1 = threading.Thread(target=run_dummy_server)
t1.start()

bot.run(os.getenv('BOT_TOKEN'))
