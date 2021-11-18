from telegram import Bot


def welcoming_self(bot: Bot, text: str, info: dict, keyboard) -> None:
    bot.send_message(
        chat_id=info['chat']['id'],
        text=text,
        reply_markup=keyboard
    )


def about_project_self(bot: Bot, text: str, info: dict, keyboard) -> None:
    photo = open(f'1.jpg', 'rb').read()

    bot.send_photo(
        chat_id=info['chat']['id'],
        photo=photo,
        caption=text,
        reply_markup=keyboard
    )

