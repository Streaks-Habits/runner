import requests
import json
import sys
import datetime
from bs4 import BeautifulSoup

def log(t):
	print("[ERROR] ", t)
	exit(1)

if len(sys.argv) != 2:
	log("Not enough OR too much arguments, waits only the athlete_id in JSON format")
parameters = json.loads(sys.argv[1])

profile_url = "https://www.strava.com/athletes/" + str(parameters["athlete_id"])
html_text = requests.get(profile_url).text
soup = BeautifulSoup(html_text, 'html.parser')

user_data_text = soup.find_all('div', attrs={
		'data-react-class': 'AthleteProfileApp'
	})[0].get('data-react-props')
user_data = json.loads(user_data_text)['recentActivities']

if not user_data:
	log("No access to profile")

moved_his_ass = False
for activity in user_data:
	if activity['startDateLocal'] == "Today":
		moved_his_ass = True

if moved_his_ass:
	print("success")
else:
	log("No acitivty today")
