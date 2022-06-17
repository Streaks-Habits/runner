import requests
import json
import sys
from bs4 import BeautifulSoup

html_text = requests.get("https://www.strava.com/athletes/14563597").text
soup = BeautifulSoup(html_text, 'html.parser')

user_data_text = soup.find_all('div', attrs={
		'data-react-class': 'AthleteProfileApp'
	})[0].get('data-react-props')
user_data = json.loads(user_data_text)

print(user_data["recentActivities"])
