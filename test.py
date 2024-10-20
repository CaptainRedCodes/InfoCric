from bs4 import BeautifulSoup
import requests


url = 'https://www.cricbuzz.com/cricket-match/live-scores'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
matches = []
for match in soup.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr'):
        title = match.find('a').text.strip()
        score = match.find('div', class_='cb-col cb-col-100 cb-scrs-wrp').text.strip()
        matches.append({'title': title, 'score': score})
