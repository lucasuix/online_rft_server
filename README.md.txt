Servidor para gerenciar RFTs ONLINE

O servidor utiliza MongoDB como o banco de dados padrão.

DB = rft_db
COLLECTION = rfts

E utiliza o djangorestframework para lidar com as solicitações como API

Utiliza-se uma IA (MiniLLM) para comparar e pesquisar os erros
que existem no banco de dados procurando assim a melhor solução

Dependências:

numpy
sentence-transformers
scikit-learn
pandas
djangorestframework
