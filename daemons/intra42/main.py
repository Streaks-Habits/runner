import json
import sys
from datetime import date
import requests
from bs4 import BeautifulSoup

USAGE_MESSAGE = 'Usage: python main.py \'{"username": "<username>", "password": "<password>"}\''

if len(sys.argv) != 2:
	print(USAGE_MESSAGE)
	sys.exit(1)

settings = json.loads(sys.argv[1])
if 'username' not in settings or 'password' not in settings:
	print(USAGE_MESSAGE)
	sys.exit(1)

# Use a requests session to store cookies
req = requests.Session()

SIGNIN_URL = 'https://signin.intra.42.fr/users/sign_in'
location_url = 'https://profile.intra.42.fr/users/' + settings['username'] + '/locations_stats'

# Retrieve authenticity_token
html_text = req.get(SIGNIN_URL).text
soup = BeautifulSoup(html_text, 'html.parser')
authenticity_token = soup.find_all('input', attrs={
	'name': 'authenticity_token'
})[0].get('value')

# Send a login request
form_data = {
	'authenticity_token': authenticity_token,
	'user[login]': settings['username'],
	'user[password]': settings['password']
}
log_request = req.post(SIGNIN_URL, data=form_data)
if 'Invalid Login or password.' in log_request.text:
	print('Invalid Login or password.')
	sys.exit(1)

# Retrieve and parse locations
locations_text = req.get(location_url).text
locations = json.loads(locations_text)

# If locations has an entry for today, then the user logged on the campus
if str(date.today()) in locations:
	print("success")
