from pymongo import MongoClient
from dotenv import load_env
import os

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PW = os.environ.get("MONGO_PW")
MONGO_DB_NAME = "TEST"
MONGO_COLLECTION = "todos"

try:
    mongo_conn = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PW}@{MONGO_HOST}")
    mongo_db = mongo_conn[MONGO_DB_NAME]
    mongo_coll = mongo_db[MONGO_COLLECTION]
except Exception as e:
    raise e
