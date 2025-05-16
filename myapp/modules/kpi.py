import json
from datetime import datetime, timedelta
from .conn import RftConn
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import re

class KPI:

    def __init__(self, data):
        self.filters = self.setup(data)
    
    def get_values(self, pipeline):
        result_list = RftConn.aggregation(pipeline)
        return [item['diferenca_em_segundos'] for item in result_list]

    def setup(self, data):
        filters = {"status": "concluida"}
        date_filters = {}
        
        if data["serialNumber"]:
            filters["serialNumber"] = data["serialNumber"]
        if data["begin_date"]:
            date_filters["$gte"] = datetime.fromisoformat(data["begin_date"]) - timedelta(hours=0)
        if data["end_date"]:
            date_filters["$lte"] = datetime.fromisoformat(data["end_date"]) - timedelta(hours=0)
        if date_filters:
            filters["sent_in"] = date_filters
        
        return filters

    def build_time_pipeline(self, start_field, end_field):
        return [
            {"$match": self.filters},
            {"$project": {
                "_id": 0,
                "diferenca_em_segundos": {
                    "$divide": [
                        {"$subtract": [f"${end_field}", f"${start_field}"]},
                        1000
                    ]
                }
            }}
        ]