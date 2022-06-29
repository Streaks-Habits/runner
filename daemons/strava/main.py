import requests
import json
import sys
from bs4 import BeautifulSoup

def log(t):
	print("[ERROR] ", t)
	exit(1)

if len(sys.argv) != 2:
	log('Usage: python main.py \'{"athlete_id": "<athlete_id>", "activities": ["<activities>"]}\'')

settings = json.loads(sys.argv[1])
if not 'athlete_id' in settings or not 'activities' in settings:
	log('Usage: python main.py \'{"athlete_id": "<athlete_id>", "activities": ["<activities>"]}\'')

profile_url = "https://www.strava.com/athletes/" + str(settings["athlete_id"])
profile_text = requests.get(profile_url).text
profile_soup = BeautifulSoup(profile_text, 'html.parser')

user_profile = profile_soup.find_all('div', attrs={'data-react-class': 'AthleteProfileApp'})
if not user_profile:
	log("Can't find user")
user_profile = user_profile[0].get('data-react-props')

user_data = json.loads(user_profile)['recentActivities']

if not user_data:
	log("Can't access user activities")

moved_his_ass = 0
for activity in user_data:
	# If activity type is in the activities or if the activities array is empty
	if activity['type'] in settings['activities'] or len(settings["activities"]) == 0:
		if activity['startDateLocal'] == "Today":
			moved_his_ass += 1

if moved_his_ass >= len(settings["activities"]):
	print("success")
