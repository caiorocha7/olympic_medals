# Olympic Medals Scraper & API

Este projeto é uma aplicação Django que faz scraping dos dados de medalhas olímpicas e disponibiliza esses dados através de uma API RESTful. A aplicação coleta informações de medalhas de países e as salva em um banco de dados, permitindo a consulta através de endpoints da API.

## 1. Funcionalidades

- **Scraping de Medalhas**: Coleta dados sobre o número de medalhas (ouro, prata, bronze) de diferentes países.
- **API RESTful**: Fornece endpoints para consultar as medalhas de cada país.
- **Django Admin**: Interface administrativa para gerenciar os dados coletados.
- **Documentação da API**: Documentação utilizando Django Rest Framework.

## 2. Requisitos

- Python 3.10+
- Django 4.0+
- Django Rest Framework
- BeautifulSoup4
- Requests

## 3. Configuração do Ambiente

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/caiorocha7/olympic_medals.git
   cd olympic_medals
   
2. Crie e ative um ambiente virtual:

   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate  # Windows

 3. Instale as dependências:

   ```bash
    pip install -r requirements.txt
```
  4. Aplique as migrações do banco de dados:
  ```bash
    python manage.py migrate
````
  5. Crie um superusuário para acessar o Django Admin:
  ```bash
    python manage.py createsuperuser
```
## 4. Executando o Scraper
Para executar o scraper e coletar os dados de medalhas, utilize o seguinte comando:
```bash
    python manage.py scrape_medals
```
## 5. Rodando a Aplicação
Para iniciar o servidor de desenvolvimento do Django, utilize:
```bash
    python manage.py runserver
Acesse a aplicação em http://127.0.0.1:8000/.
```
## 6. Endpoints da API
A API oferece os seguintes endpoints principais:

- /api/medals/top-20/: Retorna os 20 países com mais medalhas.
- /api/medals/{country_code}/: Retorna as medalhas de um país específico.
- /api/medals/: Retorna todas as medalhas cadastradas.
  
## 7. Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
