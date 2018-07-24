from pymongo import *


class Database:
    def __init__(self):
        client = MongoClient()
        self.db = client.webNutritionDB.labels

    def insert_result(self, url, result):
        self.db.insert_one({"url": url, "result":result})

    def upsert_result(self, url, label, ldict):
        self.db.update_one({"url": url}, {"$set": {
            label: ldict
        }}, True)

    def find_result(self, url):
        return self.db.find_one({"url": url})




