import json
from datetime import datetime
from .conn import RftConn
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import re


class IaPredict:
    
    modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    @staticmethod
    def predict_solution(defect, stage):

        threshold = 0.60

        rfts = RftConn.query(q_filter = {'stage': stage, 'status': 'concluida'}, limit_by = 100)
        general_list = []
        filtered_solutions_list = []
        ranked_solutions_list = []
        final_list = []

        match stage:
            case 'burnin':
                general_list = [(item['defect']['burnin_defect'], item['actions_taken']) for item in rfts]
                #Filtramos as soluções que batem com aquele defeito utilizando a IA
                filtered_solutions_list = [item[1] for item in general_list if (IaPredict.comparar_frases(defect['burnin_defect'], item[0]) > threshold)]

            case 'potencia':
                general_list = [(item['defect'], item['actions_taken']) for item in rfts]
                filtered_solutions_list = [item[1] for item in general_list if (defect == item[0])]

            case 'pre_tests':
                defect_str = IaPredict.join_defect_values({k: v for k, v in defect.items() if v})

                general_list = [
                    (IaPredict.join_defect_values(item['defect']), item['actions_taken'])
                    for item in rfts
                ]

                filtered_solutions_list = [
                     actions
                     for def_str, actions in general_list
                     if (IaPredict.comparar_frases(def_str, defect_str) > threshold) # ou `in`, `==`, `similar`, dependendo do que você quer
                ]

            case _:
                return {'toast': "STAGE não bate com nenhuma chave conhecida."}

        #Uma lista com os scores das soluções quando comparados no modelo dois a dois
        ranked_solutions_list = IaPredict.rank(filtered_solutions_list)
        #Lista com a tupla da (solução, score) e seguidamente a ordenação da lista em ordem descrescente
        final_list = [(filtered_solutions_list[i], ranked_solutions_list[i]) for i in range(len(ranked_solutions_list))]

        final_list.sort(key=lambda x: x[1], reverse=True)

        high = [item for item in final_list if item[1] > 0.75][:3]
        mid = [item for item in final_list if 0.50 < item[1] <= 0.75][:3]
        low = [item for item in final_list if item[1] <= 0.50][:3]
        
        filtered_final_list = high + mid + low

        return filtered_final_list

    @staticmethod
    def join_defect_values(defect_dict):
        return " e ".join([v.strip() for v in defect_dict.values() if v.strip()])
             
    
    @staticmethod
    def comparar_frases(frase1, frase2):
        """
        Compara semanticamente duas frases e retorna:
        - similaridade (entre 0 e 1)
        - se são consideradas semelhantes (True/False)
        """
        emb1 = IaPredict.modelo.encode(frase1, convert_to_tensor=True)
        emb2 = IaPredict.modelo.encode(frase2, convert_to_tensor=True)
        
        similaridade = float(util.cos_sim(emb1, emb2))
        print(similaridade, frase1, frase2)
        return similaridade


    @staticmethod
    def rank(in_list):
        embeddings = [IaPredict.modelo.encode(x, convert_to_tensor=True) for x in in_list]
        rank_scores = []
        
        for i in range(len(embeddings)):
            score = 0
            for j in range(len(embeddings)):
                if i != j:
                    sim = float(util.cos_sim(embeddings[i], embeddings[j]))
                    score += sim
            score = score / (len(embeddings))
            rank_scores.append(score)
            
        return rank_scores


if __name__ == '__main__':
    
    result = IaPredict.predict_solution('TCU não comunica serialmente')
    print(result)
    
