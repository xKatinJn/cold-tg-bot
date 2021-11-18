from messages_templates import OPTIONS_NUMS, MAIN_KEYBOARD_TEXT

from telegram import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup


inline_info_keyboard = InlineKeyboardMarkup(
    [
        # first line
        [InlineKeyboardButton(text=OPTIONS_NUMS['1'], callback_data='1'),
         InlineKeyboardButton(text=OPTIONS_NUMS['2'], callback_data='2')],
        [InlineKeyboardButton(text=OPTIONS_NUMS['3'], callback_data='3'),
         InlineKeyboardButton(text=OPTIONS_NUMS['4'], callback_data='4')],
    ]
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MAIN_KEYBOARD_TEXT['1']),
         KeyboardButton(text=MAIN_KEYBOARD_TEXT['2'])]
    ],
    resize_keyboard=True
)
