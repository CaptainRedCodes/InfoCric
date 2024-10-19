from django.shortcuts import render
from datetime import datetime
import requests
from .configure import API_KEY,API_HOST

def filter_stats(request):
    stats_type = request.GET.get('statsType', '')
    year = request.GET.get('year', '')
    matchtype = request.GET.get('matchtype', '')
    team = request.GET.get('team', '')



    querystring = {}
    if stats_type:
        querystring['statsType'] = stats_type
    if year:
        querystring['year'] = year
    if matchtype:
        querystring['matchType'] = matchtype
    if team:
        querystring['team'] = team

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    headers = {
        "x-rapidapi-key": API_KEY, 
        "x-rapidapi-host": API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        stats_data = response.json()

        head = stats_data.get('headers', [])
        stats_values = [item['values'] for item in stats_data.get('values', [])]

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        stats_values = []
        head = []
 

    context = {
        'stats': stats_values,
        'headers': head,
        'filter': {
            'statsType': stats_type,
            'year': year,
            'matchtype': matchtype,
            'team': team,
        },
    }

    return render(request, 'filterstats/filter.html', context)
