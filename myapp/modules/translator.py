from .rft import RFT
import requests
# Errors
# Solucao

# Stage tem que estar a par com os valores do BD
# Operador idem
# Solução idem
# 
class Server:

	def __init__(self, server_url: str = "https://ppc.tecsci.com.br/api/v1.0") -> None:
		self.server_url = server_url
		self.token = None
		self.response = None

	def login(self) -> bool:
		try:
			response = requests.post(
				self.server_url + "/auth/login",
				headers={'Content-Type': 'application/json'},
				json={'username': 'lucas.villani', 'password': '12345678'}
				)
			self.token = response.json().get("access_token")
			return True
		except Exception as e:
			print(e)
			return False

	def _get_request(self, endpoint, params=None):
		return requests.post(
			self.server_url + "/" + endpoint,
			headers= {"Authorization": f"Bearer {self.token}"},
			params = params
			).json()

	def _post_request(self, endpoint, data=None):
		return requests.post(
			self.server_url + "/" + endpoint,
			json=data,
			headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
			)



class Mount:

	trasnlates = {
		"pre_tests": 
	}

	@staticmethod
	def create(rft: RFT, has_id=False):

		data = {
            "controladora_id": controladora_id,
            "operador_id": operador_id,
            "erro_id": error_id,
            "descricao": descricao,
            "horario": horario
        }
        
		rft_data = {"controladora_id":			rft.get("serialNumber"),
					"operador_id": 	rft.get("operadorID"),
					"horario": 		rft.get("sent_in")
					"erro_id": 		{
						"etapa_id": {
							"id" : Mount.translateStage(rft.get("stage")),
							"nome" : 
						}
					}
		}

		# Dados que podem ou não tomarem parte
		if (has_id):
			rft_data["id"] = rft.get("_id")

		# Dados que precisam ser processados
		# O que acontece quando o ERRO não existe na base de dados?
		# Opa, esse ERRO veio sem ID, então é novo, adicionar ->
		# Ou eu manualmente tenho que pedir para criar um erro novo se não encontrar ele?
		