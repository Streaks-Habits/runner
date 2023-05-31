from colorama import Fore, Back, Style

from api.api import Api


def print_calendars(api: Api, args):
	calendars = api.get_calendars()

	max_len = max([len(str(cal['current_streak'])) for cal in calendars])

	for cal in calendars:
		print(Fore.BLUE + cal['_id'] + Style.RESET_ALL + ' ', end='')
		if cal['streak_expended_today']:
			print(Fore.GREEN, end='')
		else:
			print(Fore.RED, end='')

		print('🔥 ' + str(cal['current_streak']).ljust(max_len, ' ') + Style.RESET_ALL + ' ', end='')
		print(Style.BRIGHT + cal['name'] + Style.RESET_ALL + ' ')
