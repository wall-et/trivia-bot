import secret_settings
import logging

import model

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secret_settings.BOT_TOKEN)
dispatcher = updater.dispatcher

game = model.GameLogic()


def send_gif(bot, image_url, chat_id):
    bot.sendChatAction(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.sendDocument(chat_id=chat_id, document=image_url)


def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start chat #{chat_id}")

    game.add_user(chat_id)
    page_title = game.get_page_title(chat_id)
    keyboard = [[InlineKeyboardButton("Yes", callback_data='2'), InlineKeyboardButton("No", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id,
                     text=f"Welcome To The Wiki Trivia!\nWe're going to test your knowledge.\nHave you heard of {page_title.title()}?",
                     reply_markup=reply_markup)


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    res = game.test_word(text, chat_id)

    if 'win' in res:
        keyboard = [[InlineKeyboardButton("New Game", callback_data='1'),InlineKeyboardButton("Page Summary", callback_data='4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        send_gif(bot, res[res.index('url') + 3:], chat_id)
        bot.send_message(chat_id=chat_id, text=res[:res.index('url')], reply_markup=reply_markup)

    elif 'fail' in res:
        keyboard = [[InlineKeyboardButton("New Game", callback_data='1'), InlineKeyboardButton("Page Summary", callback_data='4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        send_gif(bot, res[res.index('url') + 3:], chat_id)
        bot.send_message(chat_id=chat_id, text=res[:res.index('url')], reply_markup=reply_markup)

    else:
        bot.send_message(chat_id=chat_id, text=res)


def button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    if query.data == '1':
        logger.info(f"= Got on chat #{chat_id}: pressed new game button")
        game.add_user(chat_id)
        page_title = game.get_page_title(chat_id)
        keyboard = [[InlineKeyboardButton("Yes", callback_data='2'), InlineKeyboardButton("No", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text=f"have you heard of {page_title}", reply_markup=reply_markup)


    elif query.data == '2':
        logger.info(f"= Got on chat #{chat_id}: pressed yes button")
        res = game.test_word("yes", chat_id)
        if "Try and guess" in res:
            bot.send_message(chat_id=chat_id, text=res)
        else:
            keyboard = [[InlineKeyboardButton("New Game", callback_data='1')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text=res, reply_markup=reply_markup)

    elif query.data == '3':
        logger.info(f"= Got on chat #{chat_id}: pressed no button")
        res = game.test_word("no", chat_id)
        if res == None:
            keyboard = [[InlineKeyboardButton("New Game", callback_data='1')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text="play again?", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("Yes", callback_data='2'), InlineKeyboardButton("No", callback_data='3')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text=res, reply_markup=reply_markup)

    elif query.data == '4':
        print("btn4")
        keyboard = [[InlineKeyboardButton("New Game", callback_data='1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        res=game.get_more_info(chat_id)
        bot.send_message(chat_id=chat_id, text=res, reply_markup=reply_markup)



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
logger.info("Start polling")
updater.start_polling()
