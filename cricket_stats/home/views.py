from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .configure import PROXY
proxies = {"http": PROXY}


# Function to fetch live scores from Cricbuzz
def get_live_scores():
    url = 'https://www.cricbuzz.com/cricket-match/live-scores'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers,proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')

    matches = []

    for match in soup.find_all('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm', limit=5):
        title = match.find('div', class_='cb-col-100 cb-col cb-schdl cb-billing-plans-text').text.replace('\xa0', ' ').strip()
        
        teams = match.find_all('div', class_='cb-ovr-flo cb-hmscg-tm-nm')
        team1 = teams[0].text.strip() if len(teams) > 0 else ""
        team2 = teams[1].text.strip() if len(teams) > 1 else ""
        

        scores = match.find_all('div', class_='cb-ovr-flo')
        team1_score = scores[2].text.strip() if len(scores) > 0 else ""
        team2_score = scores[4].text.strip() if len(scores) > 4 else ""
        
        
        score = f"{team1} {team1_score} vs {team2} {team2_score}"
        
        
        matches.append({'title': title, 'score': score})

    return matches

# Function to fetch latest cricket news from Cricbuzz
def cric_news():
    url = "https://www.cricbuzz.com/cricket-news/latest-news"
    response = requests.get(url,proxies=proxies)
    soup = BeautifulSoup(response.content, 'html5lib')

    news = []
    news_items = soup.find_all('a', class_='cb-nws-hdln-ancr', limit=6)


    for item in news_items:
        title = item.text.strip()
        link = "https://www.cricbuzz.com" + item['href']

        link_parts = item['href'].strip('/').split('/')
        news_id = link_parts[-2] 
        headline = link_parts[-1]

        description = item.find_next('div', class_='cb-nws-intr').text.strip()
        
        news.append({
            'title': title,
            'reallink': link,
            'description': description,
            'news_id': news_id,
            'headline':headline
        })

    return news

# View for rendering the home page with news and live scores
def home_view(request):
    news = cric_news()
    scores = get_live_scores()
    context = {
        'news': news,
        'scores': scores,
    }
    return render(request, 'home/homepage.html', context)

# Basic home page view
def home(request):
    return render(request, 'home/homepage.html')

# View for rendering the news page with detailed news content
def news_page(request,article_id,headline):
    article_url=f"https://www.cricbuzz.com/cricket-news/{article_id}/{headline}"
    content=news_text(article_url)
    context = {
        'article': content,
        'url':article_url, 
    }
    
    return render(request, 'home/newspage.html', context)

def news_text(url):
    try:
        response = requests.get(url,proxies=proxies)
        soup = BeautifulSoup(response.content, 'html5lib')

        title_element = soup.find('h1', class_='nws-dtl-hdln')
        if title_element:
            title = title_element.text.strip()
        else:
            title = 'Title not found'


        content_div = soup.find_all('p', class_='cb-nws-para')
        if content_div:
            content = [section.text.strip() for section in content_div]
        else:
            content = ['Article content not available']

        img=soup.find_all('img')
        image=img[2]
        imgurl="https://www.cricbuzz.com"+image.attrs['src']
        return {
            'title': title,
            'content': content,
            'img':imgurl
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return {'title': 'Error', 'content': ['Could not retrieve article content.']}   
