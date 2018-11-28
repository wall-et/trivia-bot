import secret_settings
import logging

import wikipedia
import re

import model

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


id_dict={}

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret_settings.BOT_TOKEN)
dispatcher = updater.dispatcher

game = model.GameLogic()



def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start chat #{chat_id}")
    value = game.get_guessing_value()
    bot.send_message(chat_id=chat_id, text=f"welcome! let’s check your knowledge. have you heard of {value.title}")

def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if text == 'no' or text == 'nope':
        value = wikipedia.page("Donald Trump")
        update.message.reply_text(f'ok. how about {value.title}')
    elif text == 'yes':
        update.message.reply_text('ok. try and guess five words from his wiki page')
    elif string_found(text, value.content)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()