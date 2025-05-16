from .rft import RFT
from .conn import RftConn
import json
from datetime import datetime

class RftController:
    
    @staticmethod
    def run(json_str, action):
        print(type(action))
        actions = {
        "nova_rft": RftController.new_rft,
        "concluir_manutencao": RftController.finish_maintenence,
        "iniciar_manutencao": RftController.start_maintenence,
        "pesquisa_personalizada": RftController.custom_search,
        "calcular_kpis": RftController.calculate_kpis
        }
        return actions[action](json_str)
        """
        try:
            return actions[action](json_str)
        except KeyError:
            return {"toast": "Ação não é válida"}
        """
    
    @staticmethod
    def new_rft(json_str):
        rft = RFT(json_str)
        response = rft.insertInDB()
        return response
    
    @staticmethod
    def finish_maintenence(json_str):
        rft = RFT()
        response = rft.finishMaintenence(json_str)
        return response
    
    @staticmethod
    def start_maintenence(json_str):
        rft = RFT()
        response = rft.startMaintenence(json_str)
        return response
        
    @staticmethod
    def custom_search(json_str):
        rft = RFT()
        rft_list = rft.customSearch(json_str)
        return rft_list

    @staticmethod
    def calculate_kpis(json_str):
        rft = RFT()
        response = rft.calculateKpis(json_str)
        return response