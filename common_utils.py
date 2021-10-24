from telegram import Update, error


def update_to_dict(update: Update) -> dict:
    result = dict()

    if update.message.text:
        text = update.message.text
    else:
        text = 'None'
    result.update({'message_text': text})

    chat = update.message.chat
    result.update({'chat': chat})

    new_chat_members = update['message']['new_chat_members']
    result.update({'new_chat_members': new_chat_members})

    return result


def private_chat_to_user_model(update: Update) -> dict:
    chat = update.message.chat
    result = {}

    result.update({'_id': chat.id})
    result.update({'username': chat.username})
    result.update({'first_name': chat.first_name})
    result.update({'last_name': chat.last_name})

    return result
