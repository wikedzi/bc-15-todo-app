import datetime

from pymongo import MongoClient

class Model():

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['todoDB']
        self.todos = self.db['todos']

