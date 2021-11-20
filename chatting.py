from telegram import Bot

from messages_templates import QUESTIONNAIRE_PERSONAL_DATA, QUESTIONNAIRE_SELF_QUESTIONS
from keyboards import yes_no_keyboard
from common_utils import get_unfilled_question_text


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
        text = get_unfilled_question_text(info)
        if text:
            bot.send_message(
                chat_id=info['chat']['id'],
                text=text,
                reply_markup=yes_no_keyboard
            )


def about_project_self(bot: Bot, text: str, info: dict, keyboard) -> None:
    photo = open(f'1.jpg', 'rb').read()

    bot.send_photo(
        chat_id=info['chat']['id'],
        photo=photo,
        caption=text,
        reply_markup=keyboard
    )

