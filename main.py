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

# install Persian model
URL_PBMM = "https://itml.cl.indiana.edu/models/fa/output_graph.pbmm"
URL_SCORER = "https://itml.cl.indiana.edu/models/fa/kenlm.scorer"
install_deepspeechmodules(URL_PBMM, URL_SCORER)

START_TXT = """
Hi {}, I'm Persian transcriber Bot.

Send an audio to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb/'),
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
    out_wav = m.audio.file_name + ".wav"
    as_wav_command = f"static_ffmpeg -y -i {media} -ac 1 -ar 16000 {out_wav}"
    os.system(as_wav_command)
    transcribed_txt = transcribe(aggressive=1, audio=out_wav, just_as_text=True)
    await msg.edit_text(transcribed_txt)
    os.remove(media)


Bot.run()
