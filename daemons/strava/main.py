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

# set every activities an not done
activities_done = {}
for activity in settings['activities']:
	activities_done[activity] = False

# set activities cone from Strava data
moved_his_ass = False
for activity in user_data:
	if activity['startDateLocal'] == 'Today':
		moved_his_ass = True
		if activity['type'] in activities_done:
			activities_done[activity['type']] = True

# check if all activities are done or if user moved his ass (if there's not activities list)
if len(settings['activities']) == 0 and moved_his_ass:
	print('success')
elif len(settings['activities']) > 0 and all(value is True for value in activities_done.values()):
	print('success')
