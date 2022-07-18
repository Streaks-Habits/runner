import json
import sys
import requests
from bs4 import BeautifulSoup


def log(message):
	print('[ERROR] ', message)
	sys.exit(1)


USAGE_MESSAGE = 'Usage: python main.py \'{"athlete_id": "<athlete_id>", "activities": ["<activities>"]}\''

if len(sys.argv) != 2:
	log(USAGE_MESSAGE)

settings = json.loads(sys.argv[1])
if 'athlete_id' not in settings or 'activities' not in settings:
	log(USAGE_MESSAGE)

PROFILE_URL = 'https://www.strava.com/athletes/' + str(settings["athlete_id"])
PROFILE_TEXT = requests.get(PROFILE_URL).text
PROFILE_SOUP = BeautifulSoup(PROFILE_TEXT, 'html.parser')

user_profile = PROFILE_SOUP.find_all('div', attrs={'data-react-class': 'AthleteProfileApp'})
if not user_profile:
	log('Can\'t find user')
user_profile = user_profile[0].get('data-react-props')

user_data = json.loads(user_profile)['recentActivities']

if not user_data:
	log('Can\'t access user activities')

moved_his_ass = 0
for activity in user_data:
	# If activity type is in the activities or if the activities array is empty
	if activity['type'] in settings['activities'] or len(settings['activities']) == 0:
		if activity['startDateLocal'] == 'Today':
			moved_his_ass += 1

if moved_his_ass >= len(settings['activities']):
	print('success')
