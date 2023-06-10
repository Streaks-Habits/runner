from colorama import Fore, Style
from rich import status
import inquirer

from api.api import Api

def print_progresses(api: Api, config, args):
	with status.Status('', spinner='point', spinner_style='blue') as s:
		progresses = api.get_progresses()

	max_len = max([len(f"{prog['current_progress']}/{prog['goal']}") for prog in progresses])

	for prog in progresses:
		print(Fore.BLUE + prog['_id'] + Style.RESET_ALL + ' ', end='')

		if prog['current_progress'] >= prog['goal']:
			print(Fore.GREEN, end='')
		else:
			print(Fore.RED, end='')

		print(f"{prog['current_progress']}/{prog['goal']}".ljust(max_len, ' ') + ' ', end='')
		print(Style.RESET_ALL, end='')

		print(Style.BRIGHT + prog['name'] + Style.RESET_ALL + ' (' + prog['recurrence_unit'] + ')')

def create_progress(api: Api, config, args):
	# Ask user for informations
		# Progress name
	name = inquirer.text(message='Progress name', validate=lambda _, x: len(x.strip()) > 0)
		# Ask for the goal
	goal = inquirer.text(message='Goal', validate=lambda _, x: x.isdigit())
		# Ask for the recurrence unit
	recurrence_unit = inquirer.list_input(message='Recurrence unit', choices=['daily', 'weekly', 'monthly', 'yearly'], default='monthly')

	new_progress = {
		'name': name.strip(),
		'goal': int(goal),
		'recurrence_unit': recurrence_unit,
	}

	with status.Status('', spinner='point', spinner_style='blue') as s:
		api.create_progress(new_progress)
	print(Style.BRIGHT + Fore.GREEN + 'Progress created!' + Style.RESET_ALL)
