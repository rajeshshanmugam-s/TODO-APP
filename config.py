from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PW = os.environ.get("MONGO_PW")
MONGO_DB_NAME = "TEST"
MONGO_COLLECTION_TODO = "todos"
MONGO_COLLECTION_USER = "users"

TOKEN_EXP = 30
TOKEN_SECRET = "secret"
TOKEN_ALGO = "HS256"

try:
    mongo_conn = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PW}@{MONGO_HOST}")
    mongo_db = mongo_conn[MONGO_DB_NAME]
    mongo_coll_todo = mongo_db[MONGO_COLLECTION_TODO]
    mongo_coll_user = mongo_db[MONGO_COLLECTION_USER]
except Exception as e:
    raise e
