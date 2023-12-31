### O que deve ser feito ainda:
- TODO mapear pelo menos 50 categorias de produtos e seus endpoints de consulta na API
- TODO gerar arquivo .CSV no lugar de .JSON e implementar lógica para criar a planilha com os produtos - Finalizado
- TODO implementar serviço de envio de e-mail contendo a planilha com os produtos encontrado - Finalizado
- TODO vincular serviço de scrap a algum framework Python e utilizar uma rota para inserir os valores via API - Finalizado (Flask Framework Python)
- TODO criar uma lógica para extrair o link de cada produto, pois a API não retorna o link do produto

### Futuramente...
-TODO vincular o serviço de scrap com agendamento de execução, utilizando AWS Lambda

![kabum](https://github.com/Nilso97/Kabum-WebScraping/assets/96146165/efd54729-0cc1-4ddc-8e5c-4901c115a8e3)

URL de consulta: http://127.0.0.1:5000/consulta-kabum/pesquisar/produto?notebooks POST
body {
	"valorMinimo": "1000", 
	"valorMaximo": "3000"
}