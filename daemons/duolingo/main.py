import requests
import json
import sys

if len(sys.argv) != 2:
	print('Usage: python main.py \'{"username": "<username>", "password": "<password>"}\'')
	quit()

settings = json.loads(sys.argv[1])
if not 'username' in settings or not 'password' in settings:
	print('Usage: python main.py \'{"username": "<username>", "password": "<password>"}\'')
	quit()

# Use a requests session to store cookies
req = requests.Session()

# Login
login_url = 'https://www.duolingo.com/login'
login_req = req.post(login_url, json={
	'login': settings['username'],
	'password': settings['password']
})
login_resp = json.loads(login_req.text)

# Check that login is successful
if 'user_id' not in login_resp:
	print(login_resp)
	quit()

# Retrieve user info
user_info_req = req.get("https://www.duolingo.com/api/1/users/show?username=" + settings['username'])
user_info_resp = json.loads(user_info_req.text)

# Check that streak as expended today
if user_info_resp['streak_extended_today']:
	print("success")
else:
	print("still not a success")
