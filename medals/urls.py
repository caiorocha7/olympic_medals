from django.urls import path
from . import views

urlpatterns = [
    path('api/medals/<str:country>/', views.get_country_medals, name='get_country_medals'),
    path('api/medals/<str:country>/sports/', views.get_country_sports_medals, name='get_country_sports_medals'),
    path('api/medals/top-20/', views.get_top_20_countries, name='get_top_20_countries'),
]
