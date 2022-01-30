import datetime
from bson import ObjectId

from pymongo import MongoClient


client = MongoClient(host='mongodb://root:example@mongo:27017/')
db = client.cold_tg_bot
users_collection = db.users
questionnaire_collection = db.questionnaire_collection


class User:
    _id: ObjectId
    username: str
    first_name: str
    last_name: str
    date_of_last_msg: datetime.datetime

    def __init__(self, **kwargs):
        if len(kwargs) == 5:
            self._id = kwargs['_id']
            self.username = kwargs['username']
            self.first_name = kwargs['first_name']
            self.last_name = kwargs['last_name']
            self.date_of_last_msg = kwargs['date_of_last_msg']
        elif 'dict' in kwargs.keys():
            document = kwargs['dict']
            self._id = document['_id']
            self.username = document['username']
            self.first_name = document['first_name']
            self.last_name = document['last_name']
            self.date_of_last_msg = document['date_of_last_msg']
        elif 'document_id' in kwargs.keys():
            document = users_collection.find_one({'_id': kwargs['document_id']})
            if document:
                self._id = document['_id']
                self.username = document['username']
                self.first_name = document['first_name']
                self.last_name = document['last_name']
                self.date_of_last_msg = document['date_of_last_msg']
            else:
                raise Exception(f'No such users._id = {kwargs["document_id"]}')
        else:
            raise Exception(f'Invalid inputs in User.__init__')

    def insert(self) -> ObjectId:
        insertion = users_collection.insert_one(self.__dict__())

        if not self._id:
            self._id = insertion.inserted_id

        return self._id

    def update(self, new_values: dict) -> None:
        if new_values:
            users_collection.update_one({'_id': self._id}, {'$set': new_values}, upsert=False)
            self.__init__(document_id=self._id)
        else:
            raise Exception('new_values variable could not be None')

    @staticmethod
    def get_user_by_id(user_id: str):
        return users_collection.find_one({'_id': user_id})

    def __dict__(self) -> dict:
        result_dict = {
            '_id': self._id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_last_msg': self.date_of_last_msg
        }
        return result_dict


class Questionnaire:
    _id: ObjectId
    is_agree: bool
    in_process: bool
    q_1: str
    q_2: str
    q_3: str
    q_4: str

    def __init__(self, _id: str, q_1: str, q_2: str, q_3: str, q_4: str, is_agree: bool, in_process: bool):
        self._id = _id
        self.q_1 = q_1
        self.q_2 = q_2
        self.q_3 = q_3
        self.q_4 = q_4
        self.is_agree = is_agree
        self.in_process = in_process

    def insert(self):
        insertion = questionnaire_collection.insert_one(self.__dict__())

        if not self._id:
            self._id = insertion.inserted_id

        return self._id

    def update(self, new_values: dict) -> None:
        if new_values:
            questionnaire_collection.update_one({'_id': self._id}, {'$set': new_values}, upsert=False)
            self.__init__(**self.get_document_by_user_id(self._id))
        else:
            raise Exception('new_values variable could not be None')

    def get_unfilled_question(self) -> str:
        if not self.q_1:
            return '1'
        if not self.q_2:
            return '2'
        if not self.q_3:
            return '3'
        if not self.q_4:
            return '4'
        return '0'

    @staticmethod
    def get_document_by_user_id(user_id: str):
        return questionnaire_collection.find_one({'_id': user_id})

    def __dict__(self) -> dict:
        result_dict = {
            '_id': self._id,
            'is_agree': self.is_agree,
            'in_process': self.in_process,
            'q_1': self.q_1,
            'q_2': self.q_2,
            'q_3': self.q_3,
            'q_4': self.q_4
        }
        return result_dict
