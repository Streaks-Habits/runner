import json
import sys
from datetime import date
import requests

if len(sys.argv) != 2:
	print('Usage: python main.py \'{"instance": "<instance>", "username": "<username>"}\'')
	sys.exit(1)

settings = json.loads(sys.argv[1])
if 'username' not in settings or 'instance' not in settings:
	print('Usage: python main.py \'{"instance": "<instance>", "username": "<username>"}\'')
	sys.exit(1)

# Retrieve user events
try:
	user_events_req = requests.get(settings["instance"] + "/api/v4/users/" + settings["username"] + "/events?action=pushed&per_page=1")
except requests.exceptions.ConnectionError:
	print("Wrong instance configuration")
	sys.exit(1)
user_events_resp = json.loads(user_events_req.text)

if "message" in user_events_resp:
	# User not found or other errors
	print(user_events_resp["message"])
	sys.exit(1)
if len(user_events_resp) == 0:
	# Not events returned
	sys.exit(1)

last_event_date = user_events_resp[0]["created_at"].split('T')[0]

# Check that streak as expended today
if str(date.today()) == last_event_date:
	print("success")
