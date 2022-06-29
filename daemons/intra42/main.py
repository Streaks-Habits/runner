import requests
import json
import sys
from bs4 import BeautifulSoup
from datetime import date

if len(sys.argv) != 2:
	print('Usage: python main.py \'{"username": "<username>", "password": "<password>"}\'')
	quit()

settings = json.loads(sys.argv[1])
if not 'username' in settings or not 'password' in settings:
	print('Usage: python main.py \'{"username": "<username>", "password": "<password>"}\'')
	quit()

# Use a requests session to store cookies
req = requests.Session()

singin_url = 'https://signin.intra.42.fr/users/sign_in'
location_url = 'https://profile.intra.42.fr/users/' + settings['username'] + '/locations_stats'

# Retrieve authenticity_token
html_text = req.get(singin_url).text
soup = BeautifulSoup(html_text, 'html.parser')
authenticity_token = soup.find_all('input', attrs={
		'name': 'authenticity_token'
	})[0].get('value')

# Send a login request
form_data = {
	'authenticity_token': authenticity_token,
	'user[login]': settings['username'],
	'user[password]':  settings['password']
}
log_request = req.post(singin_url, data = form_data)
if 'Invalid Login or password.' in log_request.text:
	print('Invalid Login or password.')
	quit()

# Retrieve and parse locations
locations_text = req.get(location_url).text
locations = json.loads(locations_text)

# If locations has an entry for today, then the user logged on the campus
if str(date.today()) in locations:
	print("success")
