import os
from urllib.parse import quote_plus
from pymongo import MongoClient

class Mongoclient:
    def __init__(self, db_collection=None):
        self.user = os.environ.get('MONGO_USER', 'central')
        self.password = os.environ.get('MONGO_PASSWORD', 'central')
        self.host = os.environ.get('MONGO_HOST', 'bert.0ixvcge.mongodb.net')
        self.db_name = os.environ.get('MONGO_DATABASE', 'central')
        self.db_collection = db_collection

        self.client = MongoClient(self._connection_string)
        self.db = self.client[self.db_name]
        if self.db_collection:
            self.collection = self.db[self.db_collection]

    @property
    def _connection_string(self):
        return "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true".format(
            quote_plus(self.user),
            quote_plus(self.password),
            self.host
        )

    def insert_one(self, document):
        if self.db_collection:
            inserted = self.collection.insert_one(document)
            return True if getattr(inserted, 'inserted_id') else False
        else:
            raise ValueError("Database collection not specified")
