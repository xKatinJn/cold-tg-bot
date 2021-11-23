import os
import logging
from random import choice
from datetime import datetime

from pprint import pprint

from models import User, Questionnaire
from common_utils import update_to_dict, private_chat_to_user_model, set_in_process_questionnaire
from messages_templates import USER_JOINED, USER_JOINED_WITHOUT_UN, WELCOMING_AND_TUTORING, OPTIONS_TEXTS, \
    MORE_QUESTIONS, QUESTIONS, USER_JOINED_ADDITIONS, PHOTO_IDS, TUTORING, ALREADY_FILLED
from keyboards import inline_info_keyboard, main_keyboard
from chatting import welcoming_self, about_project_self, questionnaire_self

from telegram import Bot, Update, InputMediaPhoto
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CallbackQueryHandler


# TODO: save answers on questions
# TODO: update answers on questions
# TODO: send answers in special chat


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

        if info['questionnaire_exist']:
            if info['questionnaire_document'].in_process:
                if info['message_text'] == 'продолжить':
                    questionnaire_self(bot, info, is_first=False, is_agree=True, is_continue=True)
                    return
                elif info['message_text'] == 'отмена':
                    set_in_process_questionnaire(info, False)
                    welcoming_self(bot, WELCOMING_AND_TUTORING, info, main_keyboard)
                    return
                else:
                    questionnaire_self(bot, info, is_first=False, is_agree=True, is_continue=False, in_process=True)
                    return

        # first join
        if info['message_text'] == '/start' or 'привет' in info['message_text']:
            welcoming_self(bot, WELCOMING_AND_TUTORING, info, main_keyboard)

        elif 'о проекте' in info['message_text']:
            about_project_self(bot, QUESTIONS, info, inline_info_keyboard)

        elif 'анкета' in info['message_text']:
            # adding new questionnaire
            if not Questionnaire.get_document_by_user_id(user_info['_id']):
                user_questionnaire = {
                    '_id': user_info['_id'],
                    'is_agree': False,
                    'in_process': True,
                    'q_1': '',
                    'q_2': '',
                    'q_3': '',
                    'q_4': ''
                }
                questionnaire = Questionnaire(**user_questionnaire)
                questionnaire.insert()
                info.update({'questionnaire_document': questionnaire})

            elif info['questionnaire_document'].get_unfilled_question() == '0':
                set_in_process_questionnaire(info, False)
                welcoming_self(bot, ALREADY_FILLED + TUTORING, info, main_keyboard)
                return
            else:
                set_in_process_questionnaire(info, True)

            if info['chat']['id'] == Questionnaire.get_document_by_user_id(info['chat']['id']):
                questionnaire_self(bot, info, False)
            else:
                questionnaire_self(bot, info, True)


def handle_query(update: Update, call: CallbackContext):
    callback_data = update.callback_query.data

    # changing message text by callback_data value
    if callback_data in ['1', '2', '3', '4']:
        input_photo = InputMediaPhoto(media=PHOTO_IDS[callback_data], caption=MORE_QUESTIONS+'\n'*2+QUESTIONS)

        bot.edit_message_media(
            chat_id=update.callback_query.from_user.id,
            message_id=update.callback_query.message.message_id,
            media=input_photo,
            reply_markup=inline_info_keyboard
        )
        bot.answerCallbackQuery(
            callback_query_id=update.callback_query.id,
            text='Ответ на вопрос на фото :)'
        )


def start() -> None:
    logging.basicConfig(
        filename='logs.log',
        filemode='a',
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
