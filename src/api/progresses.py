from colorama import Fore, Style

from api.api import Api

def print_progresses(api: Api, args):
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
