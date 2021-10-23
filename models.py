import datetime
from bson import ObjectId

from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.cold_tg_bot
users_collection = db.users


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

    def update(self, new_values: dict):
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
