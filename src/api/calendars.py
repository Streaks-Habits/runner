from colorama import Fore, Back, Style
from rich import status
import inquirer

from api.api import Api
from api.exceptions import NotFoundException


def print_calendars(api: Api, config, args):
	with status.Status('', spinner='point', spinner_style='blue') as s:
		try:
			calendars = api.get_calendars()
		except NotFoundException:
			print(Style.BRIGHT + 'No calendars found!' + Style.RESET_ALL)
			return
		except Exception as e:
			print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
			return

	max_len = max([len(str(cal['current_streak'])) for cal in calendars])

	for cal in calendars:
		print(Fore.BLUE + cal['_id'] + Style.RESET_ALL + ' ', end='')
		if cal['streak_expended_today']:
			print(Fore.GREEN, end='')
		else:
			print(Fore.RED, end='')

		print('🔥 ' + str(cal['current_streak']).ljust(max_len, ' ') + Style.RESET_ALL + ' ', end='')
		print(Style.BRIGHT + cal['name'] + Style.RESET_ALL + ' ')

def create_calendar(api: Api, config, args):
	# Ask user for informations
		# Calendar name
	name = inquirer.text(message='Calendar name', validate=lambda _, x: len(x.strip()) > 0)
		# Ask if user wants to enable notifications
	notifications = inquirer.checkbox(message='Enable notifications?', choices=['Reminders', 'Congratulations'], default=['Reminders', 'Congratulations'])
		# Ask for the agenda
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	agenda = inquirer.checkbox(message='Agenda (disabled days will be frozen)', choices=days, default=days[:5])

	new_calendar = {
		'name': name.strip(),
		'agenda': [day in agenda for day in days],
		'notifications': {
			'reminders': 'Reminders' in notifications,
			'congrats': 'Congratulations' in notifications,
		}
	}

	with status.Status('', spinner='point', spinner_style='blue') as s:
		api.create_calendar(new_calendar)
	print(Style.BRIGHT + Fore.GREEN + 'Calendar created!' + Style.RESET_ALL)

def delete_calendar(api: Api, config, args):
	if not 'calendar_id' in args or args.calendar_id is None:
		# Ask user for calendar id
		calendar_id = inquirer.text(message='Calendar id', validate=lambda _, x: len(x.strip()) > 0)
	else:
		calendar_id = args.calendar_id

	with status.Status('', spinner='point', spinner_style='blue') as s:
		try:
			api.delete_calendar(calendar_id)
		except Exception as e:
			print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
			return

	print(Style.BRIGHT + Fore.GREEN + 'Calendar deleted!' + Style.RESET_ALL)
