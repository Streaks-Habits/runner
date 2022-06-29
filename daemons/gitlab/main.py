import requests
import json
import sys
from datetime import date

if len(sys.argv) != 2:
	print('Usage: python main.py \'{"instance": "<instance>", "username": "<username>"}\'')
	quit()

settings = json.loads(sys.argv[1])
if not 'username' in settings or not 'instance' in settings:
	print('Usage: python main.py \'{"instance": "<instance>", "username": "<username>"}\'')
	quit()

# Retrieve user events
try:
	user_events_req = requests.get(settings["instance"] + "/api/v4/users/" + settings["username"] + "/events?action=pushed&per_page=1")
except requests.exceptions.ConnectionError:
	print("Wrong instance configuration")
	quit()
user_events_resp = json.loads(user_events_req.text)

if "message" in user_events_resp:
	# User not found or other errors
	print(user_events_resp["message"])
	quit()
if len(user_events_resp) == 0:
	# Not events returned
	quit()

last_event_date = user_events_resp[0]["created_at"].split('T')[0]

# Check that streak as expended today
if (str(date.today()) == last_event_date):
	print("success")
