from django.shortcuts import render
import requests

# Create your views here.
def serieslist(request):
    apikey = "84a8ce67-a812-4ac9-bf9a-66ab06c97709"
    response=requests.get(f"https://api.cricapi.com/v1/series?apikey={apikey}&offset=0")

    if response.status_code == 200:
        series_data = response.json().get('data',[])
    else:
        series_data=[]
    
    return render(request,'serieslist/series.html',{'series':series_data})