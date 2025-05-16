# from .config import db_config
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone, timedelta

# Connect to MongoDB (default host and port)
# client = MongoClient(db_config["address"])
client = MongoClient("mongodb://localhost:27017/")
# Create or connect to a database
# db = client[db_config["database_name"]]
db = client["rft_db"]

class RftConn:
    
    __rfts = db["rfts"]
    
    @staticmethod
    def insert(rft_data):
        rft_data.pop("_id") # Para não escrever uma _id vazia para o BD
        inserted = RftConn.__rfts.insert_one(rft_data)
        print(f'RFT inserida com id {inserted}')
    
    @staticmethod
    def update(rft_id, rft_data):
        rft_data.pop("_id")
        updated = RftConn.__rfts.update_one({"_id": ObjectId(rft_id)}, {"$set": rft_data})
        print(f'RFT {updated} atualizada com {rft_data}')
    
    # Função master de consulta para ser reutilizada sempre
    @staticmethod
    def query(sort_by = "_id", limit_by = 50, order = "newer", offset = 0, q_filter = None):
        if q_filter is None:
            q_filter = {}

        get_order = {"newer": -1, "older": 1}
        sort_order = get_order.get(order, -1)
        
        query_result = (
            RftConn.__rfts.find(q_filter)
            .sort(sort_by, sort_order)
            .skip(offset)
            .limit(limit_by)
        )
        result_list = []
        for data in query_result:
            data["_id"] = str(data["_id"])
            result_list.append(data)
            
        return result_list

    @staticmethod
    def aggregation(pipeline):
        return list(RftConn.__rfts.aggregate(pipeline))


