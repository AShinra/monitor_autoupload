import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATA_MONGO_URI = os.getenv("DATA_MONGO_URI")


def connect_to_mongo():
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is not set. Add it to your .env file.")
    client = MongoClient(MONGO_URI)
    return client["zeno_db"]

def write_to_file(new_data):
    file_name = f'timelogs.txt'
    with open(file_name, "a") as file:
        file.write(f'{new_data}\n')

def connect_to_data():
    if not DATA_MONGO_URI:
        raise RuntimeError("DATA_MONGO_URI is not set. Add it to your .env file.")
    client = MongoClient(DATA_MONGO_URI)
    db = client['autoupload']
    collection = db['data']
    return collection
