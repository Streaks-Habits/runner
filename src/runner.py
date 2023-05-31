import yaml
import importlib
import argparse
from pprint import pprint
from datetime import date, timedelta
import requests
from colorama import Fore, Back, Style
from rich import status

parser = argparse.ArgumentParser()
parser.add_argument('--service', help='Service to run (default: *)', default='*')
parser.add_argument('--force', help='When used with --service, run the specified service even if it is disabled. Has no impact if --service is not specified or equal to *.', action='store_true')
parser.add_argument('--reset', help='Reset service(s) data', action='store_true')
parser.add_argument('--start', help='Start date, ISO format, will run the service for every day between start and today (default: today)', default=str(date.today()))

args = parser.parse_args()

def set_state(config, service, state, for_date):
	API_ENDPOINT = f'{config["instance"]}/api/v1/calendars/state'

	for cal in service['calendars']:
		if state == '':
			continue
		resp = requests.post(
			f'{API_ENDPOINT}/{cal}/{state}?for={for_date}',
			headers={'x-api-key': config['api_key']},
		)
		if resp.status_code != 200:
			print('Error while setting state for calendar ' + cal)
			print(resp.status_code)
			print(resp.text)

def set_days(config, service, start, end):
	print(Fore.BLUE + Style.BRIGHT + service['name'] + Style.RESET_ALL)

	with status.Status('', spinner='point', spinner_style='blue') as s:
		mod = importlib.import_module('.main', package='services.' + service['type'])

		# Get data
		data = mod.get_data(service, start)

		# Loop over days
		day = start
		while day <= end:
			is_success = False
			# Loop over data
			for d in data:
				if d['date'].date() == day:
					if mod.is_success(service, d):
						is_success = True
						break

			# Set state with api
			set_state(config, service, 'success' if is_success else '', day)

			if is_success:
				print(Fore.GREEN + Style.BRIGHT + '\t' + str(day) + ' ✅ Success' + Style.RESET_ALL)
			else:
				print(Fore.YELLOW + Style.BRIGHT + '\t' + str(day) + ' ❎ Fail' + Style.RESET_ALL)
			day += timedelta(days=1)

with open('config.yml') as f:
	config = yaml.safe_load(f)

	for service in config['services']:
		if args.service != '*' and service['name'] != args.service:
			continue
		if args.service != '*' and service['enable'] is False and args.force is False:
			print('Service ' + service['name'] + ' is disabled (use --force to run it anyway)')
			continue

		if args.start:
			# Check if the date is valid
			try:
				start = date.fromisoformat(args.start)
			except ValueError:
				print(Fore.RED + Style.BRIGHT + 'Invalid date format, use ISO format (YYYY-MM-DD)' + Style.RESET_ALL)
				exit(1)

			set_days(config, service, start, date.today())
		else:
			set_days(config, service, date.today(), date.today())

