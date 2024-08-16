from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Country, Sport, Medal

class MedalAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Criar dados de exemplo
        self.country = Country.objects.create(name='EUA', code='USA', gold=40, silver=44, bronze=42)
        self.sport = Sport.objects.create(name='Atletismo')
        self.medal = Medal.objects.create(country=self.country, sport=self.sport, gold=10, silver=12, bronze=8)

    def test_get_country_medals(self):
        url = reverse('get_country_medals', kwargs={'country': 'USA'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['gold'], 40)
        self.assertEqual(response.data['silver'], 44)
        self.assertEqual(response.data['bronze'], 42)

    def test_get_country_sports_medals(self):
        url = reverse('get_country_sports_medals', kwargs={'country': 'USA'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sport'], 'Atletismo')
        self.assertEqual(response.data[0]['gold'], 10)
        self.assertEqual(response.data[0]['silver'], 12)
        self.assertEqual(response.data[0]['bronze'], 8)

    def test_get_top_20_countries(self):
        url = reverse('get_top_20_countries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Temos apenas 1 país no setup
        self.assertEqual(response.data[0]['country'], 'EUA')
        self.assertEqual(response.data[0]['medals'][0]['sport'], 'Atletismo')
        self.assertEqual(response.data[0]['medals'][0]['gold'], 10)
        self.assertEqual(response.data[0]['medals'][0]['silver'], 12)
        self.assertEqual(response.data[0]['medals'][0]['bronze'], 8)
