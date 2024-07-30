import os
from urllib.parse import quote_plus
from pymongo import MongoClient

class Mongoclient:
    def __init__(self, db_collection=None):
        self.host = os.environ.get('MONGO_HOST', '0.0.0.0')
        self.port = int(os.environ.get('MONGO_PORT', '27017'))
        self.connect_with_user = os.environ.get('CONNECT_WITH_USER', 'False') == 'True'

        if self.connect_with_user:
            self.user = os.environ.get('MONGO_USER', 'central')
            self.password = os.environ.get('MONGO_PASSWORD', 'central')

        self.client = MongoClient(self._connection_string)
        self.db_name = os.environ.get('MONGO_DATABASE', 'central')
        self.db_collection = db_collection

        self.db = self.client[self.db_name]
        if self.db_collection:
            self.collection = self.db[self.db_collection]

    @property
    def _connection_string(self):
        if self.connect_with_user:
            return "mongodb://{0}:{1}@{2}:{3}/?retryWrites=true&w=majority".format(
                quote_plus(self.user),
                quote_plus(self.password),
                self.host,
                self.port
            )
        else:
            return "mongodb://{0}:{1}/?retryWrites=true&w=majority".format(
                self.host,
                self.port
            )

    def insert_one(self, document):
        if self.db_collection:
            inserted = self.collection.insert_one(document)
            return True if getattr(inserted, 'inserted_id') else False
        else:
            raise ValueError("Database collection not specified")
