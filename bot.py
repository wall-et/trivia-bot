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

    game.add_user(chat_id)
    value = game.get_value(chat_id)

    bot.send_message(chat_id=chat_id, text=f"welcome! let’s check your knowledge. have you heard of {value.title}")


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    res = game.test_word(text, chat_id)
    if res == 'win' or res == 'lose':
        keyboard = [[InlineKeyboardButton("new game")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(res,reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=chat_id, text=res)


def button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    logger.info(f"= Got on chat #{chat_id}: pressed new game button")

    game.add_user(chat_id)
    value = game.get_value(chat_id)
    
    bot.send_message(chat_id=chat_id, text=f"have you heard of {value.title}")



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()