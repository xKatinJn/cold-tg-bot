from messages_templates import OPTIONS_TEXTS

from telegram import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup


inline_info_keyboard = InlineKeyboardMarkup(
    [
        # first line
        [InlineKeyboardButton(text=OPTIONS_TEXTS['1'], callback_data='1'),
         InlineKeyboardButton(text=OPTIONS_TEXTS['2'], callback_data='2')],
        [InlineKeyboardButton(text=OPTIONS_TEXTS['3'], callback_data='3'),
         InlineKeyboardButton(text=OPTIONS_TEXTS['4'], callback_data='4')],

        # second line
        [InlineKeyboardButton(text=OPTIONS_TEXTS['5'], callback_data='5'),
         InlineKeyboardButton(text=OPTIONS_TEXTS['6'], callback_data='6')],
        [InlineKeyboardButton(text=OPTIONS_TEXTS['7'], callback_data='7'),
         InlineKeyboardButton(text=OPTIONS_TEXTS['8'], callback_data='8')],
    ]
)
