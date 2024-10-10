
import requests
from django.shortcuts import render

def matchlist(request):
    apikey = "84a8ce67-a812-4ac9-bf9a-66ab06c97709"
    response = requests.get(f"https://api.cricapi.com/v1/matches?apikey={apikey}&offset=0")


    if response.status_code == 200:
        match_data = response.json().get('data', [])  
    else:
        match_data = []

    print(match_data,flush=True)
