from telegram import Bot

from messages_templates import QUESTIONNAIRE_PERSONAL_DATA, QUESTIONNAIRE_SELF_QUESTIONS, FILLED_SUCCESSFULLY, ADMINS, \
    TUTORING, PHOTO_IDS

from keyboards import yes_no_keyboard, main_keyboard
from common_utils import get_unfilled_question_text, set_in_process_questionnaire, prepare_questionnaire_result


def welcoming_self(bot: Bot, text: str, info: dict, keyboard) -> None:
    bot.send_message(
        chat_id=info['chat']['id'],
        text=text,
        reply_markup=keyboard
    )


def questionnaire_self(bot: Bot, info: dict, is_first: bool, is_agree: bool = None, is_continue: bool = None,
                       in_process: bool = None) -> None:
    if is_first:
        text = QUESTIONNAIRE_PERSONAL_DATA
        set_in_process_questionnaire(info, True)
        bot.send_message(
            chat_id=info['chat']['id'],
            text=text,
            reply_markup=yes_no_keyboard
        )
    elif is_agree and is_continue:
        text = get_unfilled_question_text(info)
        bot.send_message(
            chat_id=info['chat']['id'],
            text=text,
            reply_markup=yes_no_keyboard
        )
    elif in_process:
        q_obj = info['questionnaire_document']
        q_num = q_obj.get_unfilled_question()

        # check if there unfilled question
        if q_num != '0':
            q_obj.update({f'q_{q_num}': info['message_text']})

        text = get_unfilled_question_text(info)

        if text:
            bot.send_message(
                chat_id=info['chat']['id'],
                text=text,
                reply_markup=yes_no_keyboard
            )
        else:
            send_questionnaire_result(bot, info)
            set_in_process_questionnaire(info, False)
            bot.send_message(
                chat_id=info['chat']['id'],
                text=FILLED_SUCCESSFULLY+TUTORING,
                reply_markup=main_keyboard
            )


def about_project_self(bot: Bot, text: str, info: dict, keyboard) -> None:
    photo = open(f'1.jpg', 'rb').read()

    bot.send_photo(
        chat_id=info['chat']['id'],
        photo=PHOTO_IDS['1'],
        caption=text,
        reply_markup=keyboard
    )


def send_questionnaire_result(bot: Bot, info: dict) -> None:
    text = prepare_questionnaire_result(info)

    for admin_id in ADMINS:
        bot.send_message(
            chat_id=admin_id,
            text=text
        )
