from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Country, Medal

@api_view(['GET'])
def get_country_medals(request, country):
    """
    Retorna o total de medalhas (ouro, prata, bronze) para o país especificado.
    """
    try:
        # Busca o país pelo nome, ignorando a caixa alta/baixa
        country_obj = Country.objects.get(name__iexact=country)
        # Cria a resposta com os dados do país
        return Response({
            'country': country_obj.name,
            'gold': country_obj.gold,
            'silver': country_obj.silver,
            'bronze': country_obj.bronze,
        })
    except Country.DoesNotExist:
        # Retorna uma mensagem de erro se o país não for encontrado
        return Response({'error': 'Country not found'}, status=404)

@api_view(['GET'])
def get_country_sports_medals(request, country):
    """
    Lista os esportes nos quais o país especificado ganhou medalhas,
    juntamente com a contagem de medalhas para cada esporte.
    """
    try:
        # Busca o país pelo nome, ignorando a caixa alta/baixa
        country_obj = Country.objects.get(name__iexact=country)
        # Busca todas as medalhas do país em diferentes esportes
        medals = Medal.objects.filter(country=country_obj)
        result = {}
        # Popula o resultado com a contagem de medalhas por esporte
        for medal in medals:
            result[medal.sport.name] = {
                'gold': medal.gold,
                'silver': medal.silver,
                'bronze': medal.bronze,
            }
        # Retorna a resposta com o dicionário de esportes e medalhas
        return Response(result)
    except Country.DoesNotExist:
        # Retorna uma mensagem de erro se o país não for encontrado
        return Response({'error': 'Country not found'}, status=404)

@api_view(['GET'])
def get_top_20_countries(request):
    """
    Retorna os 20 primeiros países no quadro de medalhas,
    incluindo o número de medalhas (ouro, prata, bronze) conquistadas em cada esporte.
    """
    # Busca os 20 países com o maior número de medalhas de ouro, seguido por prata e bronze
    countries = Country.objects.all().order_by('-gold', '-silver', '-bronze')[:20]
    result = []
    # Para cada país, busca as medalhas por esporte
    for country in countries:
        sports = Medal.objects.filter(country=country)
        sports_medals = {
            sport.sport.name: {
                'gold': sport.gold,
                'silver': sport.silver,
                'bronze': sport.bronze,
            } for sport in sports
        }
        # Adiciona o país e seus esportes ao resultado final
        result.append({
            'country': country.name,
            'medals': {
                'gold': country.gold,
                'silver': country.silver,
                'bronze': country.bronze,
            },
            'sports': sports_medals,
        })
    # Retorna a resposta com a lista dos 20 países e suas medalhas
    return Response(result)
