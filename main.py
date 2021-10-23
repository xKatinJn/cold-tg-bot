import os
import logging

from common_utils import update_to_dict
from messages_templates import USER_JOINED, USER_JOINED_WITHOUT_UN

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters


API_TOKEN = os.getenv('BOT_API_TOKEN')

bot = Bot(token=API_TOKEN)


def message_handler(update: Update, context: CallbackContext) -> None:
    info = update_to_dict(update)
    print(info)
    # ===============
    # CHAT PROCESSING
    # ===============

    if info['chat']['type'] in ['supergroup']:
        if info['new_chat_members']:
            new_user_name = info['new_chat_members'][0]['username']
            if new_user_name:
                bot.send_message(info['chat']['id'], USER_JOINED.format(new_user_name))
            else:
                new_user_name = info['new_chat_members'][0]['first_name'] + ' ' + info['new_chat_members'][0]['last_name']
                bot.send_message(info['chat']['id'], USER_JOINED_WITHOUT_UN.format(new_user_name))

        bot.send_message(info['chat']['id'], info['message_text'])

    # ===========================
    # PRIVATE MESSAGES PROCESSING
    # ===========================

    else:
        bot.send_message(info['chat']['id'], info['message_text'])


def start() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    updater = Updater(
        token=API_TOKEN
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start()
