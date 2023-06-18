import yaml
import argparse
from datetime import date

from api.api import Api
from api.calendars import (
    print_calendars,
    create_calendar,
    delete_calendar,
    edit_calendar,
)
from api.progresses import print_progresses, create_progress, delete_progress
from runner import run_service

################
# General parser
################
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

##################
# Calendars parser
##################
parser_calendars = subparsers.add_parser("calendars")
subparsers_calendars = parser_calendars.add_subparsers()
parser_calendars.set_defaults(
    func=lambda x, y, z: parser_calendars.print_help()
)
# Calendars list parser
parser_calendars_list = subparsers_calendars.add_parser("list")
parser_calendars_list.set_defaults(func=print_calendars)
# Calendars create parser
parser_calendars_create = subparsers_calendars.add_parser("add")
parser_calendars_create.add_argument(
    "--name", help="Calendar name", required=False
)
parser_calendars_create.add_argument(
    "--disable-reminders",
    help="Disable reminders notifications",
    required=False,
    action="store_true",
)
parser_calendars_create.add_argument(
    "--disable-congrats",
    help="Disable congratulations notifications",
    required=False,
    action="store_true",
)
parser_calendars_create.add_argument(
    "--agenda", help="Agenda (disabled days will be frozen)", required=False
)
parser_calendars_create.set_defaults(func=create_calendar)
# Delete calendar parser.
parser_calendars_delete = subparsers_calendars.add_parser("delete")
parser_calendars_delete.add_argument(
    "calendar_id",
    help="Calendar ID to delete (Optionnal)",
    nargs="?",
    default=None,
)
parser_calendars_delete.set_defaults(func=delete_calendar)
# Edit calendar parser.
parser_calendars_edit = subparsers_calendars.add_parser("edit")
parser_calendars_edit.add_argument(
    "calendar_id",
    help="Calendar ID to edit (Optionnal)",
    nargs="?",
    default=None,
)
parser_calendars_edit.add_argument(
    "--name", help="Calendar name to set", required=False
)
parser_calendars_edit.add_argument(
    "--disable-reminders",
    help="Disable reminders notifications",
    required=False,
    action="store_true",
)
parser_calendars_edit.add_argument(
    "--enable-reminders",
    help="Enable reminders notifications",
    required=False,
    action="store_true",
)
parser_calendars_edit.add_argument(
    "--disable-congrats",
    help="Disable congratulations notifications",
    required=False,
    action="store_true",
)
parser_calendars_edit.add_argument(
    "--enable-congrats",
    help="Enable congratulations notifications",
    required=False,
    action="store_true",
)
parser_calendars_edit.add_argument(
    "--agenda",
    help="Agenda to set (disabled days will be frozen)",
    required=False,
)
parser_calendars_edit.set_defaults(func=edit_calendar)

###################
# Progresses parser
###################
parser_progresses = subparsers.add_parser("progresses")
subparsers_progresses = parser_progresses.add_subparsers()
parser_progresses.set_defaults(
    func=lambda x, y, z: parser_progresses.print_help()
)
# Progresses list parser
parser_progresses_list = subparsers_progresses.add_parser("list")
parser_progresses_list.set_defaults(func=print_progresses)
# Progresses create parser
parser_progresses_create = subparsers_progresses.add_parser("add")
parser_progresses_create.set_defaults(func=create_progress)
# Delete progress parser.
parser_progresses_delete = subparsers_progresses.add_parser("delete")
parser_progresses_delete.add_argument(
    "progress_id",
    help="Progress ID to delete (Optionnal)",
    nargs="?",
    default=None,
)
parser_progresses_delete.set_defaults(func=delete_progress)

###############
# Runner parser
###############
parser_runner = subparsers.add_parser("runner")
parser_runner.add_argument(
    "--service", help="Service to run (default: all)", default=True
)
parser_runner.add_argument(
    "--force",
    help="When used with --service, \
          run the specified service even if it is disabled. \
          Has no impact if --service is not specified or equal to *.",
    action="store_true",
)
parser_runner.add_argument(
    "--reset", help="Reset service(s) data", action="store_true"
)
parser_runner.add_argument(
    "--start",
    help="Start date, ISO format, will run the service for every day between \
          start and today (default: today)",
    default=str(date.today()),
)
parser_runner.set_defaults(func=run_service)

with open("config.yml") as f:
    config = yaml.safe_load(f)

    api = Api(config["api_key"], config["instance"])

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(api, config, args)
    else:
        parser.print_help()
