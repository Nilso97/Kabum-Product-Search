### O que deve ser feito ainda:
- TODO mapear pelo menos 50 categorias de produtos e seus endpoints de consulta na API
- TODO gerar arquivo .xlsx no lugar de jaon e implementar lógica para criar a planilha com os produtos encontrados - Concluído ✅
- TODO implementar serviço de envio de e-mail contendo a planilha com os produtos encontrados - Concluído ✅
- TODO vincular serviço de scrap a algum framework Python e utilizar uma rota para inserir os valores via API - Concluído ✅ (Flask Framework Python)
- TODO criar uma lógica para extrair o link de cada produto, pois a API não retorna o link do produto

### Futuramente...
-TODO vincular o serviço de scrap com agendamento de execução, utilizando AWS Lambda

### Rodando o projeto: 
URL: http://127.0.0.1:5000/consulta-kabum/pesquisar/produto/monitor-gamer<br>
HTTP method [POST]<br>
body: {
	"valorMinimo": "1000", 
	"valorMaximo": "3000"
}
