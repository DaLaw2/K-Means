import os
from K_Means import K_Means
from pymongo import MongoClient

if __name__ == "__main__":
    connection = MongoClient("mongodb://172.18.0.3:27017/")
    database = connection["K-Means"]
    collection = database["K-Means Data"]
    while True:
        for document in  collection.find():
            if document["status"] == "congestion":
                os.system(f"python3 K_Means.py -r {document['rows']} -c {document['cols']} -k {document['clusters']} -n {document['saveName']} /var/www/html/data/{document['saveName']}.xlsx /var/www/html/result")
                if os.path.exists(f"/var/www/html/result/{document['saveName']}.log"):
                    collection.update_one({"saveName": f"{document['saveName']}"}, {"$set": {"status": "error"}})
                else:
                    collection.update_one({"saveName": f"{document['saveName']}"}, {"$set": {"status": "success"}})
                