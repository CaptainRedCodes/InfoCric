import requests
from django.shortcuts import render
from .configure import API_HOST,API_KEY

API_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
API_KEY = API_KEY
API_HOST = API_HOST

def search_cricketer(request):
    print("search_cricketer view called")  # Debugging line
    stats = None
    player_details = None
    player_career = None

    if request.method == 'POST':
        cricketer_name = request.POST.get('cricketer_name')
        cricketer_info = get_cricketer_id(cricketer_name)

        if cricketer_info:
            player_id = cricketer_info['id']
            stats = cricketer_info
            player_details = get_player_details(player_id)
            player_career = career_of_player(player_id)
            player_stats=stats_of_player(player_id)

            return render(request, 'stats/search.html', {
                'stats': stats,
                'player_details': player_details,
                'player_career': player_career,
                "player_stats":player_stats
            })

def get_cricketer_id(cricketer_name):
    url = API_URL
    querystring = {"plrN": cricketer_name}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json().get('player', [])
        if data:
            return data[0]  # Return the first player's info
        else:
             raise ValueError("Cric noot found")
    else:
        status=response.json().get('error',{}).get('message','API exhausted')
        error_message=status
        print(error_message)

    return None

def get_player_details(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        status=response.json().get('error',{}).get('message','Player Details Unavailable')
        error_message=status
        print(error_message)
    return None

def career_of_player(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/career"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        player_data = response.json()
        formats = player_data.get('values', [])
        app_index = player_data.get('appIndex', {})

        return {
            'formats': formats,
            'seoTitle': app_index.get('seoTitle', ''),
            'webURL': app_index.get('webURL', '')
        }
    else:
        status=response.reason
        error_message=status
        print(error_message)

    return None

def stats_of_player(player_id):
    batting_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
    bowling_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
def process_stats(data):
    # Extract headers (formats like Test, ODI, T20, IPL)
    headers = data.get('headers', [])
    
    # Extract rows containing stat categories (Matches, Innings, Runs, etc.)
    stats_values = data.get('values', [])

    processed_stats = []


    for stat in stats_values:
        category_values = stat.get('values', [])
        processed_stat = {
                'name': stat.get('values')[0],  # Get the stat category name (e.g., Matches, Innings)
            }
        for i in range(1,len(headers)):
                processed_stat[headers[i]] = category_values[i]
        processed_stats.append(processed_stat)
    
    return processed_stats

def stats_of_player(player_id):
    batting_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
    bowling_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    batting_stats = []
    bowling_stats = []

    try:
        batting_response = requests.get(batting_url, headers=headers)
        batting_response.raise_for_status()
        batting_data = batting_response.json()  
        batting_stats = process_stats(batting_data)
    except requests.RequestException as e:
        print(f"Error fetching batting stats: {str(e)}")

    try:
        bowling_response = requests.get(bowling_url, headers=headers)
        bowling_response.raise_for_status()
        bowling_data = bowling_response.json()
        bowling_stats = process_stats(bowling_data)
    except requests.RequestException as e:
        print(f"Error fetching bowling stats: {str(e)}")

    return {
        'batting_stats': batting_stats,  
        'bowling_stats': bowling_stats    
    }
