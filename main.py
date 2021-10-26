import os
import logging
from random import choice
from datetime import datetime

from pprint import pprint

from models import User
from common_utils import update_to_dict, private_chat_to_user_model
from messages_templates import USER_JOINED, USER_JOINED_WITHOUT_UN, WELCOMING_AND_TUTORING, OPTIONS_TEXTS, \
    MORE_QUESTIONS, QUESTIONS, USER_JOINED_ADDITIONS
from keyboards import inline_info_keyboard

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CallbackQueryHandler


API_TOKEN = os.getenv('BOT_API_TOKEN')

bot = Bot(token=API_TOKEN)


def message_handler(update: Update, context: CallbackContext) -> None:
    # transform update
    info = update_to_dict(update)
    pprint(info)

    # ===============
    # GROUP CHATS PROCESSING
    # ===============

    if info['chat']['type'] in ['supergroup']:
        if info['new_chat_members']:
            # iterating on new chat members
            for new_user in info['new_chat_members']:
                new_user_name = new_user['username']

                # welcoming new user in chat
                if new_user_name:
                    bot.send_message(info['chat']['id'],
                                     USER_JOINED.format(new_user_name)+choice(USER_JOINED_ADDITIONS))
                else:
                    new_user_name = new_user['first_name'] + ' ' \
                                    + new_user['last_name']
                    bot.send_message(info['chat']['id'],
                                     USER_JOINED_WITHOUT_UN.format(new_user_name)+choice(USER_JOINED_ADDITIONS))

    # ===========================
    # PRIVATE MESSAGES PROCESSING
    # ===========================

    else:
        # getting info about user
        user_info = private_chat_to_user_model(update)
        pprint(user_info)

        # adding new user in database
        if not User.get_user_by_id(user_info['_id']):
            user_info.update({'date_of_last_msg': datetime.utcnow()})
            new_user = User(dict=user_info)
            new_user.insert()

        # first join
        if info['message_text'] == '/start':
            bot.send_message(info['chat']['id'],
                             text=WELCOMING_AND_TUTORING+QUESTIONS, reply_markup=inline_info_keyboard)


def handle_query(update: Update, call: CallbackContext):
    callback_data = update.callback_query.data

    if callback_data in ['1', '2', '3', '4']:
        bot.edit_message_text(
            chat_id=update.callback_query.from_user.id,
            message_id=update.callback_query.message.message_id,
            text=OPTIONS_TEXTS[callback_data]+'\n'*3+MORE_QUESTIONS+QUESTIONS,
            reply_markup=inline_info_keyboard
        )
        # bot.send_message(update.callback_query.from_user.id, text=OPTIONS_TEXTS[callback_data])
        # bot.send_message(update.callback_query.from_user.id, text=MORE_QUESTIONS+QUESTIONS,
        #                  reply_markup=inline_info_keyboard)

    print('cb data is ', callback_data)


def start() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    updater = Updater(
        token=API_TOKEN
    )
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=handle_query))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start()
