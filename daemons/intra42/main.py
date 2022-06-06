import requests
import json
import sys
from bs4 import BeautifulSoup
from datetime import date

if len(sys.argv) != 3:
	print("Usage: python main.py <login> <password>")
	quit()

login=sys.argv[1]
password=sys.argv[2]

# Use a requests session to store cookies
req = requests.Session()

singin_url = 'https://signin.intra.42.fr/users/sign_in'
location_url = 'https://profile.intra.42.fr/users/ocartier/locations_stats'

# Retrieve authenticity_token
html_text = req.get(singin_url).text
soup = BeautifulSoup(html_text, 'html.parser')
authenticity_token = soup.find_all('input', attrs={
		'name': 'authenticity_token'
	})[0].get('value')

# Send a login request
form_data = {
	'authenticity_token': authenticity_token,
	'user[login]': login,
	'user[password]': password
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
else:
	print("still not a success")
