import yaml
import argparse

from api.api import Api
from api.calendars import print_calendars
from api.progresses import print_progresses

# General parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Calendars parser
parser_calendars = subparsers.add_parser('calendars')
subparsers_calendars = parser_calendars.add_subparsers()
parser_calendars.set_defaults(func=lambda x, y: parser_calendars.print_help())
	# Calendars list parser
parser_calendars_list = subparsers_calendars.add_parser('list')
parser_calendars_list.set_defaults(func=print_calendars)

# Progresses parser
parser_progresses = subparsers.add_parser('progresses')
subparsers_progresses = parser_progresses.add_subparsers()
parser_progresses.set_defaults(func=lambda x, y: parser_progresses.print_help())
	# Progresses list parser
parser_progresses_list = subparsers_progresses.add_parser('list')
parser_progresses_list.set_defaults(func=print_progresses)

with open('config.yml') as f:
	config = yaml.safe_load(f)

	api = Api(config['api_key'], config['instance'])

	args = parser.parse_args()
	if hasattr(args, 'func'):
		args.func(api, args)
	else:
		parser.print_help()
