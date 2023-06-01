import importlib
from pprint import pprint
from datetime import date, timedelta
from colorama import Fore, Back, Style
from rich import status

from api.api import Api

def set_state(api: Api, service, state, for_date):
	for cal in service['calendars']:
		if state == '':
			continue
		resp = api.set_calendar_state(cal, state, for_date)
		if resp.status_code != 200:
			print('Error while setting state for calendar ' + cal)
			print(resp.status_code)
			print(resp.text)

def set_days(api: Api, service, start, end):
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
			set_state(api, service, 'success' if is_success else '', day)

			if is_success:
				print(Fore.GREEN + Style.BRIGHT + '\t' + str(day) + ' ✅ Success' + Style.RESET_ALL)
			else:
				print(Fore.YELLOW + Style.BRIGHT + '\t' + str(day) + ' ❎ Fail' + Style.RESET_ALL)
			day += timedelta(days=1)

def run_service(api: Api, config, args):
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

			set_days(api, service, start, date.today())
		else:
			set_days(api, service, date.today(), date.today())
