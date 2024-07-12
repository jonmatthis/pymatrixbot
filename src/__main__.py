import os

import simplematrixbotlib as botlib
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

BOT_PREFIX = '!'

config = botlib.Config()
config.emoji_verify = True
config.ignore_unverified_devices = False
# config.encryption_enabled = True

creds = botlib.Creds(os.getenv('HOMESERVER_URL'), os.getenv('BOT_USERNAME'), os.getenv('BOT_PASSWORD'))

model = ChatAnthropic(model="claude-3-sonnet-20240229")
BOTERMELON_SYSTEM_PROMPT_CONTENT = """
- I am an agent speaking to a human.
- I approach subjects in a rigorous, factual, academic, level-headed tone.
- I vehemently support Palestinian liberation in all its forms.
- I do not tolerate misrepresentations of history by Israeli propaganda.
- I speak with the collective knowledge and rhetorical prowess of such scholars as Norman Finkelstein, Rashid Khalidi, Edward Said, and Ilan Pappé
- I strongly prioritize archaeological evidence for historical accuracy to distinguish facts from biblical narratives and other mythologies.
- Be precise.
- Keep answers brief, just a paragraph or two.
"""
BOTERMELON_SYSTEM_PROMPT = SystemMessage(content=BOTERMELON_SYSTEM_PROMPT_CONTENT)

bot = botlib.Bot(creds, config=config)


@bot.listener.on_message_event
async def echo(room, message):
    """
    Example command that "echoes" arguements.
    Usage:
    example_user- !echo say something
    echo_bot- say something
    """
    match = botlib.MessageMatch(room, message, bot, BOT_PREFIX)
    if match.is_not_from_this_bot() and match.prefix():
        if match.command("echo"):
            await bot.api.send_text_message(room.room_id, " ".join(arg for arg in match.args()))
        elif match.command("chat"):
            human_message = HumanMessage(content=" ".join(arg for arg in match.args()))
            print(f"Received message: {human_message.content}")
            ai_response = model.invoke([BOTERMELON_SYSTEM_PROMPT, human_message])
            print(f"AI response: {ai_response}")
            await bot.api.send_text_message(room.room_id, ai_response.content)


bot.run()
