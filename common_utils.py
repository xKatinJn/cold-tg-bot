from telegram import Update
from models import Questionnaire
from messages_templates import QUESTIONNAIRE_SELF_QUESTIONS, QUESTIONNAIRE_RESULT


def update_to_dict(update: Update) -> dict:
    result = dict()

    if update.message.text:
        text = update.message.text.lower()
    else:
        text = 'None'
    result.update({'message_text': text})

    chat = update.message.chat
    result.update({'chat': chat})

    new_chat_members = update['message']['new_chat_members']
    result.update({'new_chat_members': new_chat_members})

    try:
        questionnaire_document = Questionnaire(**Questionnaire.get_document_by_user_id(chat.id))
        result.update({'questionnaire_exist': True})
    except TypeError:
        questionnaire_document = None
        result.update({'questionnaire_exist': False})
    result.update({'questionnaire_document': questionnaire_document})

    return result


def private_chat_to_user_model(update: Update) -> dict:
    chat = update.message.chat
    result = {}

    result.update({'_id': chat.id})
    result.update({'username': chat.username})
    result.update({'first_name': chat.first_name})
    result.update({'last_name': chat.last_name})

    return result


def set_in_process_questionnaire(info: dict, state: bool) -> None:
    quest_obj: Questionnaire = info['questionnaire_document']
    quest_obj.update({'in_process': state})


def get_unfilled_question_text(info: dict) -> str:
    quest_obj: Questionnaire = info['questionnaire_document']
    num = quest_obj.get_unfilled_question()
    if num != '0':
        return QUESTIONNAIRE_SELF_QUESTIONS[num]
    else:
        return ''


def prepare_questionnaire_result(info: dict) -> str:
    quest_obj: Questionnaire = info['questionnaire_document']

    result = QUESTIONNAIRE_RESULT.format(quest_obj.q_1, info['chat']['username'], quest_obj.q_4) + '\n'

    for i in range(2, 4):
        quest = QUESTIONNAIRE_SELF_QUESTIONS[str(i)]
        ans = quest_obj.__getattribute__(f'q_{i}')
        result += f'Вопрос: "{quest}"\n\nОтвет: {ans}\n\n'

    return result
