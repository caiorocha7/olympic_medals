from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from medals.models import Country  # Importa seu modelo Country

class Command(BaseCommand):
    help = "Scrape Olympic medal data and save to the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting web scraping...")  # Log para indicar o início do processo

        # URL da página que contém o quadro de medalhas
        url = 'https://olympics.com/pt/paris-2024/medalhas'  # Certifique-se de que esta URL está correta

        # Tenta fazer a requisição à página
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            self.stdout.write(self.style.SUCCESS("Successfully connected to the URL"))  # Log de sucesso na conexão
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve the webpage: {e}"))  # Log de erro
            return  # Encerra a execução em caso de erro na conexão

        # Analisa o conteúdo HTML da página usando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Procura todos os elementos que representam as linhas de países no quadro de medalhas
        countries_data = soup.find_all('div', {'data-testid': 'noc-row'})

        if not countries_data:
            self.stdout.write(self.style.ERROR("No country data found on the page."))  # Log de erro se não encontrar dados
            return

        # Itera sobre cada país encontrado na página
        for country in countries_data:
            try:
                # Extrai as informações desejadas para cada país
                position = country.find('span', {'class': 'emotion-srm-1m7a47k'}).text
                flag_img = country.find('img', {'class': 'euzfwma3'}).get('src')
                code = country.find('span', {'class': 'euzfwma4'}).text
                name = country.find('span', {'class': 'euzfwma5'}).text
                gold = int(country.find_all('span', {'class': 'emotion-srm-81g9w1'})[0].text)
                silver = int(country.find_all('span', {'class': 'emotion-srm-81g9w1'})[1].text)
                bronze = int(country.find_all('span', {'class': 'emotion-srm-81g9w1'})[2].text)
                total = int(country.find('span', {'class': 'emotion-srm-5nhv3o'}).text)

                # Log das informações extraídas
                self.stdout.write(self.style.NOTICE(
                    f"Processing {name}: Gold={gold}, Silver={silver}, Bronze={bronze}, Total={total}"
                ))

                # Salva ou atualiza o país no banco de dados
                country_obj, created = Country.objects.get_or_create(name=name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added new country: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated existing country: {name}"))

                # Atualiza os dados do país no banco de dados
                country_obj.gold = gold
                country_obj.silver = silver
                country_obj.bronze = bronze
                country_obj.total = total
                country_obj.save()

            except Exception as e:
                # Log de qualquer erro encontrado ao processar um país
                self.stdout.write(self.style.ERROR(f"Failed to process country data: {e}"))
        
        # Log de conclusão do processo de scraping
        self.stdout.write(self.style.SUCCESS("Web scraping completed successfully!"))
