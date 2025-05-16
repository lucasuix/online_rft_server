from .rft import RFT

class InputVerifier:
    
    @staticmethod
    def compatibilidade(data):
        return True
        # return list(data.keys()) == RFT.__slots__
    
    @staticmethod
    def serialNumber(serialNumber: str):
        return len(serialNumber) == 13 and serialNumber.isnumeric()
    
    @staticmethod
    def operadorID(operadorID: str):
        return operadorID.isnumeric()
        
    @staticmethod
    def defect(defect: str):
        return len(defect) <= 255
    
    @staticmethod
    def step(step: str):
        return True
    
    @staticmethod
    def obs(obs: str):
        return True
             










if __name__ == "__main__":
    
    print("Iniciando testes...")
    
    data = {"serialNumber": "abcdefghijklm", "elephant": "Rat", "operadorID": "q9", "step": "", "defect": "Somewhere over a raibow."}
    
    print("Compatibilidade de String 1 - Elemento a mais:")
    if (InputVerifier.compatibilidade(data)):
        print("Não Passou")
    else:
        print("Passou")
    
    print("Serial Number deve ser numérico e possuir 13 caracteres:")
    
    if (InputVerifier.serialNumber(data["serialNumber"])):
        print(f'Não Passou {data["serialNumber"]} expected FALSE')
    else:
        print(f'Passou {data["serialNumber"]}, FALSE is correct')
    
    
    data["serialNumber"] = "123123123"
    if (InputVerifier.serialNumber(data["serialNumber"])):
        print(f'Não Passou {data["serialNumber"]} expected FALSE')
    else:
        print(f'Passou {data["serialNumber"]} FALSE is correct')
    
    data["serialNumber"] = "1231231231231"
    if (InputVerifier.serialNumber(data["serialNumber"])):
        print(f'Passou {data["serialNumber"]} TRUE is correct')
    else:
        print(f'Não Passou {data["serialNumber"]} expected TRUE')
    
    print("OperadorID deve ser numérico:")
    if (InputVerifier.operadorID(data["operadorID"])):
        print(f'Não Passou {data["operadorID"]} expected FALSE')
    else:
        print(f'Passou {data["operadorID"]} FALSE is correct')
    
    data["operadorID"] = "19"
    if (InputVerifier.operadorID(data["operadorID"])):
        print(f'Passou {data["operadorID"]} TRUE is correct')
    else:
        print(f'Não passou {data["operadorID"]} expected TRUE')
