from telegram import Update, error


def update_to_dict(update: Update) -> dict:
    result = dict()

    try:
        text = update.message.text
        result.update({'message_text': text})
    except error.BadRequest:
        print("Message is NONE")

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
