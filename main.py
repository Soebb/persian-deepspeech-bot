import os
from pydeepspeech.transcribe import transcribe
from pydeepspeech.install_models import install_deepspeechmodules
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

Bot = Client(
    "PersianTranscriberBot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)


install_deepspeechmodules(

START_TXT = """
Hi {}, I'm Persian transcriber Bot.

Send an audio to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb/persian-transcriber-bot'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )



@Bot.on_message(filters.private & filters.audio)
async def from_tg_files(_, m):
    msg = await m.reply("Downloading..")
    media = await m.download()
    await msg.edit_text("Processing..")
    output_name = os.path.basename(media).rsplit('.', 1)[0] + ".txt"
    transcribe(media, output_name)
    await m.reply_document(output_name)
    os.remove(media)


Bot.run()
