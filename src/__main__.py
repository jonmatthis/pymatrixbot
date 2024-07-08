import os

from dotenv import load_dotenv
import simplematrixbotlib as botlib

load_dotenv()

BOT_PREFIX = '!'

homeserver=os.getenv('HOMESERVER_URL')
username=os.getenv('BOT_USERNAME')
password=os.getenv('BOT_PASSWORD')
creds = botlib.Creds(homeserver, username, password)

bot = botlib.Bot(creds)
bot.run()
@bot.listener.on_message_event
async def echo(room, message):
    """
    Example command that "echoes" arguements.
    Usage:
    example_user- !echo say something
    echo_bot- say something
    """
    match = botlib.MessageMatch(room, message, bot, BOT_PREFIX)
    await bot.api.send_text_message(room.room_id, " ".join(arg for arg in match.args()))

bot.run()