from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_live_scores():
        
    # URL of the page
    url = 'https://www.cricbuzz.com/cricket-match/live-scores'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    matches = []

    for match in soup.find_all('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm',limit=5):
        try:
            title = match.find('a', class_='text-hvr-underline').text.strip()
            score = match.find('div', class_='cb-scr-wll-chvrn').text.strip()
            matches.append({'title': title, 'score': score})
        except AttributeError:
            continue
    return matches



def cric_news():
    url = "https://www.cricbuzz.com/cricket-news/latest-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    news = []
    news_items = soup.find_all('a', class_='cb-nws-hdln-ancr', limit=6)
    for item in news_items:
        title = item.text.strip()
        link = "https://www.cricbuzz.com" + item['href']
        description = item.find_next('div', class_='cb-nws-intr').text.strip()
        
        news.append({'title': title, 'link': link, 'description': description})
    return news

def home_view(request):
    news = cric_news()
    scores = get_live_scores()
    context = {
        'news': news,
        'scores': scores,
    }
    return render(request, 'home/homepage.html', context)

def home(request):
    return render(request,'home/homepage.html')
