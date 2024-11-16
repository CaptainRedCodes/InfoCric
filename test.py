import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/img/v1/i1/c231889/i.jpg"

headers = {
	"x-rapidapi-key": "0ecbd5d0f3mshc507ec066e66c50p115f52jsndbe98791a8dc",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

try:
    data = response.json()
    print(data)
except requests.exceptions.JSONDecodeError:
    print("Response is not JSON. Raw response:", response.text)

