from django.shortcuts import render
import requests
from .configure import API_KEY

# Create your views here.
def serieslist(request):
    apikey = API_KEY
    response=requests.get(f"https://api.cricapi.com/v1/series?apikey={apikey}&offset=0")

    if response.status_code == 200:
        series_data = response.json().get('data',[])
    else:
        series_data=[]
    
    return render(request,'serieslist/series.html',{'series':series_data})