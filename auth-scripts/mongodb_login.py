"""Python authentication script for mongodb."""
from pymongo import MongoClient

client = MongoClient("mongodb://root:passord@192.168.2.8:27017")
db = client.admin
try:
    db.command("serverStatus")
except Exception as e:
    print(e)
else:
    print("You are connected!")
client.close()
