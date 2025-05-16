import json
import numpy as np
from datetime import datetime, timedelta
from .conn import RftConn
from .ia_predict import IaPredict
from .kpi import KPI



class RFT:

    __slots__ = ["_id",
                "serialNumber",
                "operadorID",
                "stage",
                "defect",
                "sent_in",
                "start_time",
                "end_time",
                "obs",
                "actions_taken",
                "tecnicoID",
                "status"]
                
    def __init__(self, json_str = None):
        self._id = ""
        self.serialNumber = ""
        self.operadorID = ""
        self.stage = ""
        self.defect = ""
        self.obs = ""
        self.sent_in = self.get_time()
        self.start_time = ""
        self.end_time = ""
        self.actions_taken = ""
        self.tecnicoID = ""
        self.status = ""
        
        if json_str is not None:
            self.setAttrFromJson(json_str)
    
    # Server
    def get(self, attribute):
        return getattr(self, attribute)
    
    def set(self, attribute, value):
        setattr(self, attribute, value)
    
    def setAttrFromJson(self, json_str):
        data = self.loadJson(json_str)
        for key, value in data.items():
            setattr(self, key, value)
    
    def setJsonFromAttr(self):
        data = {slot: getattr(self, slot) for slot in self.__slots__}
        return json.dumps(data)
    
    def toDict(self):
        dictionary = {}
        for value in self.__slots__:
            dictionary[value] = self.get(value)
        return dictionary
    
    def loadJson(self, json_str):
        if type(json_str) is str:
            return json.loads(json_str)
        else:
            return json_str
    
    def json_Integrity(self, data):
        result = True
        print(data)
        for key in data:
            result &= key in RFT.__slots__
        return result

    def json_IntegrityForNew(self, data):
        result = True
        print(data)
        for key in data:
            result &= key in RFT.__slots__
        # MonkeyFix for bad user input
        if (data["serialNumber"] == "" or data["stage"] == "" or data["operadorID"] == ""):
            result = False
        if (len(data["serialNumber"]) != 13 or data["serialNumber"].isnumeric() == False):
            result = False
        return result
        
    # DB
    def insertInDB(self):
        rft_data = self.toDict()
        if(self.json_IntegrityForNew(rft_data)):
            RftConn.insert(rft_data)
            return {"toast": "RFT criada com sucesso"}
        else:
            return {"toast" : "RFT possui dados inválidos", "bad_input": True}
    
    def updateInDB(self, json_str):
        rft_data = self.loadJson(json_str)
        if(self.json_Integrity(rft_data)):
            RftConn.update(rft_data["_id"], rft_data)
            return {"toast": "Alterações salvas"}
        else:
            return {"toast": "RFT possui dados inválidos"}
    
    # User 
    def startMaintenence(self, json_str):
        data = self.loadJson(json_str)
        solutions_list = []
        
        serialNumber = data["serialNumber"]
        rfts = RftConn.query(q_filter = {"serialNumber": serialNumber}, limit_by = 1) #Busca a RFT mais recente para aquela TCU
        
        if rfts:
            last_rft = rfts[0]
            
            if (data['ai_assist']):
                solutions_list = IaPredict.predict_solution(last_rft['defect'], last_rft['stage'])
            
            if (last_rft["start_time"] == ""):
                last_rft["start_time"] = self.get_time()
                self.updateInDB({"_id": last_rft["_id"], "start_time": last_rft["start_time"]})
            
            #Aqui só retornar um response, que tenha a last_rft e ia_predictions separado
            return {"rft": last_rft, "solutions_list": solutions_list}
        else:
            return {"toast": "Não há nenhuma RFT aberta para essa TCU"}
    
    def customSearch(self, json_str):
        print(json_str)
        data = self.loadJson(json_str)
        filters = {}
        date_filters = {}
        
        if data["status"]:
            filters["status"] = data["status"]
        if data["serialNumber"]:
            filters["serialNumber"] = data["serialNumber"]
        if data["begin_date"]:
            date_filters["$gte"] = datetime.fromisoformat(data["begin_date"]) - timedelta(hours=0)
        if data["end_date"]:
            date_filters["$lte"] = datetime.fromisoformat(data["end_date"]) - timedelta(hours=0)
        if date_filters:
            filters["sent_in"] = date_filters
        
        rfts = RftConn.query(q_filter = filters, order = data["order"])
        return rfts
    
    def finishMaintenence(self, json_str):
        rft_data = self.loadJson(json_str)

        if (rft_data["tecnicoID"] == "" or rft_data["actions_taken"] == ""):
            return {"toast": "Campos Faltando!", "bad_input": True }
        rft_data["end_time"] = self.get_time()
        return self.updateInDB(rft_data)
        
    def calculateKpis(self, json_str):
        data = self.loadJson(json_str)
        query = data['query']
        kpis = data['kpis']
        kpi = KPI(query)

        result = {}

        if "conclusao_media" in kpis:
            pipeline = kpi.build_time_pipeline("sent_in", "end_time")
            values_list = kpi.get_values(pipeline)
            media = np.mean(values_list)
            result['conclusao_media'] = media

        if "conclusao_mediana" in kpis:
            pipeline = kpi.build_time_pipeline("sent_in", "end_time")
            values_list = kpi.get_values(pipeline)
            median = np.median(values_list)
            result['conclusao_mediana'] = median

        if "manutencao_media" in kpis:
            pipeline = kpi.build_time_pipeline("start_time", "end_time")
            values_list = kpi.get_values(pipeline)
            media = np.mean(values_list)
            result['manutencao_media'] = media

        if "manutencao_mediana" in kpis:
            pipeline = kpi.build_time_pipeline("start_time", "end_time")
            values_list = kpi.get_values(pipeline)
            median = np.median(values_list)
            result['manutencao_mediana'] = median

        return result

    # Para resolver o problema dos timezones
    def get_time(self):
        date = datetime.now() - timedelta(hours=3)
        return date