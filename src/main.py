import yaml
import argparse
from datetime import date

from api.api import Api
from api.calendars import print_calendars
from api.progresses import print_progresses
from runner import run_service

# General parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Calendars parser
parser_calendars = subparsers.add_parser('calendars')
subparsers_calendars = parser_calendars.add_subparsers()
parser_calendars.set_defaults(func=lambda x, y, z: parser_calendars.print_help())
	# Calendars list parser
parser_calendars_list = subparsers_calendars.add_parser('list')
parser_calendars_list.set_defaults(func=print_calendars)

# Progresses parser
parser_progresses = subparsers.add_parser('progresses')
subparsers_progresses = parser_progresses.add_subparsers()
parser_progresses.set_defaults(func=lambda x, y, z: parser_progresses.print_help())
	# Progresses list parser
parser_progresses_list = subparsers_progresses.add_parser('list')
parser_progresses_list.set_defaults(func=print_progresses)

# Runner parser
parser_runner = subparsers.add_parser('runner')
parser_runner.add_argument('--service', help='Service to run (default: *)', default='*')
parser_runner.add_argument('--force', help='When used with --service, run the specified service even if it is disabled. Has no impact if --service is not specified or equal to *.', action='store_true')
parser_runner.add_argument('--reset', help='Reset service(s) data', action='store_true')
parser_runner.add_argument('--start', help='Start date, ISO format, will run the service for every day between start and today (default: today)', default=str(date.today()))
parser_runner.set_defaults(func=run_service)

with open('config.yml') as f:
	config = yaml.safe_load(f)

	api = Api(config['api_key'], config['instance'])

	args = parser.parse_args()
	if hasattr(args, 'func'):
		args.func(api, config, args)
	else:
		parser.print_help()
