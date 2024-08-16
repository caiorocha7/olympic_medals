from django.core.management.base import BaseCommand
import requests
from medals.models import Country  # Certifique-se de que este seja o modelo correto

class Command(BaseCommand):
    help = "Fetch Olympic medal data from API and save to the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to fetch data from API...")

        url = 'https://apis.codante.io/olympic-games/countries'

        try:
            self.stdout.write("Attempting to connect to the API...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            self.stdout.write(self.style.SUCCESS("Successfully connected to the API"))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve the data from API: {e}"))
            return

        # Tente acessar a chave 'data' dentro da resposta JSON
        try:
            response_json = response.json()
            countries_data = response_json.get('data', [])  # Acessa a lista de países
            if not countries_data:
                self.stdout.write(self.style.ERROR("No data found under 'data' key"))
                return
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Failed to parse JSON data: {e}"))
            return

        for country in countries_data:
            try:
                # Confirma se cada item é um dicionário
                if not isinstance(country, dict):
                    self.stdout.write(self.style.ERROR(f"Unexpected data format: {country}"))
                    continue

                code = country['id']
                name = country['name']
                gold = int(country['gold_medals'])
                silver = int(country['silver_medals'])
                bronze = int(country['bronze_medals'])
                total = gold + silver + bronze  # Calcula o total de medalhas

                self.stdout.write(self.style.NOTICE(
                    f"Processing {name}: Gold={gold}, Silver={silver}, Bronze={bronze}, Total={total}"
                ))

                country_obj, created = Country.objects.get_or_create(code=code, defaults={
                    'name': name,
                    'gold': gold,
                    'silver': silver,
                    'bronze': bronze,
                })
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added new country: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated existing country: {name}"))
                    country_obj.gold = gold
                    country_obj.silver = silver
                    country_obj.bronze = bronze
                    country_obj.save()

            except KeyError as e:
                self.stdout.write(self.style.ERROR(f"Missing expected key in data: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to process country data: {e}"))

        self.stdout.write(self.style.SUCCESS("Data fetching completed successfully!"))
