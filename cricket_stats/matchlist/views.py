import requests
from django.shortcuts import render
from datetime import datetime
from .configure import API_KEY
def matchlist(request):
    apikey=API_KEY
    response = requests.get(f"https://api.cricapi.com/v1/currentMatches?apikey={apikey}&offset=0")

    if response.status_code == 200:
        match_data = response.json().get('data', [])  
    else:
        match_data = []

    formatted_matches = []
    
    for match in match_data:
        match_date = match.get('dateTimeGMT')  # Using 'dateTimeGMT' key

        if match_date:
            try:
                
                date_obj = datetime.strptime(match_date, "%Y-%m-%dT%H:%M:%S")
                
                formatted_date = date_obj.strftime("%B %d, %Y, %I:%M %p")  
                match['formatted_date'] = formatted_date
            except ValueError:
                match['formatted_date'] = "Invalid date"

        formatted_matches.append(match)

    return render(request, 'matchlist/match.html', {'matches': formatted_matches})
