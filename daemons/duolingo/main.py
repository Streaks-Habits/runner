import requests
import json
import sys

if len(sys.argv) != 3:
	print("Usage: python main.py <login> <password>")
	quit()

login=sys.argv[1]
password=sys.argv[2]

# Use a requests session to store cookies
req = requests.Session()

# Login
login_url = 'https://www.duolingo.com/login'
login_req = req.post(login_url, json={
	'login': login,
	'password': password
})
login_resp = json.loads(login_req.text)

# Check that login is successful
if 'user_id' not in login_resp:
	print(login_resp)
	quit()

# Retrieve user info
user_info_req = req.get("https://www.duolingo.com/api/1/users/show?username=" + login)
user_info_resp = json.loads(user_info_req.text)

# Check that streak as expended today
if user_info_resp['streak_extended_today']:
	print("success")
else:
	print("still not a success")
