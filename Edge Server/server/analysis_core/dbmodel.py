import sys
sys.path.append('/home/pc/edge_service/v1/config/')
import settings

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import datetime

db_connection_string = settings.db_url
client = MongoClient(db_connection_string)
edge_db = client["edge"]
sensor_collection = edge_db[settings.collection_name]
test_col = edge_db["test"]


def fetch_by_query(query, projection):
  return sensor_collection.find(query, projection)


def fetch_data_batch(time):
  query = {
    "date": {"$gte": str(datetime.datetime.utcnow() - datetime.timedelta(minutes = time))}
    }
  projection = {"data":1, "label":1,"_id":0}
  return fetch_by_query(query, projection)


def insert(data):
  sensor_collection.insert_one(data)

def insert_test(data):
  test_col.insert_one(data)

def run():
  try:
    client.admin.command('ping')
    #edge_db = client["edge"]
    #sensor_collection = edge_db["sensors"]
    print("--> Database is connected!")
  except ConnectionFailure:
    print("--> Database is not connected!")

