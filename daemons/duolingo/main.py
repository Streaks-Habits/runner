import json
import sys
import requests
import re
from datetime import date
from datetime import datetime
from datetime import timedelta

if len(sys.argv) != 2:
	print('Usage: python main.py \'{"username": "<username>", "password": "<password>"}\'')
	sys.exit(1)

settings = json.loads(sys.argv[1])
if 'username' not in settings or 'password' not in settings or 'goal' not in settings or settings['goal'] not in ['streak', 'xp']:
	xpreg = re.match(r'^(\d.)xp$', settings['goal'])
	if (xpreg is not None):
		# change xp goal to given number
		settings['goal'] = 'xp'
		settings['goal_xp'] = int(xpreg.group(1))
	else:
		print('Usage: python main.py \'{"username": "<username>", "password": "<password>", "goal": "<streak|[num]xp>"}\'')
		sys.exit(1)

# Use a requests session to store cookies
req = requests.Session()

# Login
login_req = req.post('https://www.duolingo.com/login', json={
	'login': settings['username'],
	'password': settings['password']
})
login_resp = json.loads(login_req.text)

# Check that login is successful
if 'user_id' not in login_resp:
	print(login_resp)
	sys.exit(1)

# Retrieve user info
user_info_req = req.get('https://www.duolingo.com/api/1/users/show?username=' + settings['username'])
user_info_resp = json.loads(user_info_req.text)

if settings['goal'] == 'streak':
	# Check that streak as expended today
	if user_info_resp['streak_extended_today']:
		print('success')
elif settings['goal'] == 'xp':
	# Check that xp goals is reached today
	xp_goal = user_info_resp['daily_goal']
	# if xp goal is given, use that instead
	if 'goal_xp' in settings:
		xp_goal = settings['goal_xp']
	today_xp = 0

	lasts_activities = user_info_resp['calendar']
	today_midnight = datetime.combine(date.today(), datetime.max.time()).timestamp() * 1000
	yesterday_midnight = datetime.combine(date.today() - timedelta(days=1), datetime.max.time()).timestamp() * 1000
	for activity in lasts_activities:
		if activity['datetime'] > yesterday_midnight and activity['datetime'] < today_midnight:
			today_xp += activity['improvement']

	if today_xp >= xp_goal:
		print('success')
