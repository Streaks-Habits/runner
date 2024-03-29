from datetime import date
from colorama import Fore, Style
from rich import status
import inquirer

from api.api import Api
from api.exceptions import NotFoundException


def print_calendars(api: Api, config, args):
    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            calendars = api.get_calendars()
        except NotFoundException:
            print(Style.BRIGHT + "No calendars found!" + Style.RESET_ALL)
            return
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return

    max_len = max([len(str(cal["current_streak"])) for cal in calendars])

    for cal in calendars:
        try:
            cal_info = api.get_month(cal["_id"], date.today().strftime("%Y-%m"))
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return
        day_str = date.today().strftime("%Y-%m-%d")

        # calendar id color (blue if enabled, grey if disabled)
        if cal["enabled"]:
            print(Fore.BLUE, end="")
        else:
            print(Fore.LIGHTBLACK_EX, end="")
        print(cal["_id"] + Style.RESET_ALL + " ", end="")

        # if success
        if cal["streak_expended_today"]:
            print(Fore.GREEN, end="")
        # if frozen
        elif (
            "days" in cal_info
            and day_str in cal_info["days"]
            and cal_info["days"][day_str] == "freeze"
        ):
            print(Fore.BLUE, end="")
        # if fail
        else:
            print(Fore.RED, end="")

        print(
            "🔥 "
            + str(cal["current_streak"]).ljust(max_len, " ")
            + Style.RESET_ALL
            + " ",
            end="",
        )
        print(Style.BRIGHT + cal["name"] + Style.RESET_ALL + " ")


def create_calendar(api: Api, config, args):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # If one of the arguments is not None
    has_args = False
    for arg in vars(args):
        if getattr(args, arg) is not None and arg != "func":
            if arg in ["disable_reminders", "disable_congrats", "enable", "disable"]:
                if getattr(args, arg):
                    has_args = True
            else:
                has_args = True

    # If no arguments are specified, ask user for informations
    if not has_args:
        # Calendar name
        name = inquirer.text(
            message="Calendar name", validate=lambda _, x: len(x.strip()) > 0
        )
        # Ask if user wants to enable notifications
        notifications = inquirer.checkbox(
            message="Enable notifications?",
            choices=["Reminders", "Congratulations"],
            default=["Reminders", "Congratulations"],
        )
        # Ask for the agenda
        agenda = inquirer.checkbox(
            message="Agenda (disabled days will be frozen)",
            choices=days,
            default=days[:5],
        )
        # Ask if the calendar should be enabled
        enabled = inquirer.confirm(message="Enable calendar?", default=True)
    # If arguments are specified, check that at least the name is specified
    elif "name" not in args or args.name is None:
        print(Style.BRIGHT + Fore.RED + "You must specify a name!" + Style.RESET_ALL)
        return
    # If arguments are specified, and there is a name, check the arguments
    else:
        if "name" not in args or args.name is None or len(args.name.strip()) == 0:
            print(
                Style.BRIGHT + Fore.RED + "You must specify a name!" + Style.RESET_ALL
            )
            return
        name = args.name

        notifications = ["Reminders", "Congratulations"]
        if "disable_reminders" in args and args.disable_reminders:
            notifications.remove("Reminders")
        if "disable_congrats" in args and args.disable_congrats:
            notifications.remove("Congratulations")

        agenda = days[:5]
        if "agenda" in args and args.agenda is not None:
            agenda = []
            for day in args.agenda.split(","):
                day = day.strip().capitalize()
                if day in days:
                    agenda.append(day)
                else:
                    print(
                        Style.BRIGHT
                        + Fore.RED
                        + "Invalid day: "
                        + day
                        + Style.RESET_ALL
                    )
                    return

        enabled = True
        if "enable" in args and args.enable:
            enabled = True
        if "disable" in args and args.disable:
            enabled = False

    new_calendar = {
        "name": name.strip(),
        "agenda": [day in agenda for day in days],
        "notifications": {
            "reminders": "Reminders" in notifications,
            "congrats": "Congratulations" in notifications,
        },
        "enabled": enabled,
    }

    with status.Status("", spinner="point", spinner_style="blue"):
        api.create_calendar(new_calendar)
    print(Style.BRIGHT + Fore.GREEN + "Calendar created!" + Style.RESET_ALL)


def delete_calendar(api: Api, config, args):
    if "calendar_id" not in args or args.calendar_id is None:
        # Ask user for calendar id
        calendar_id = inquirer.text(
            message="Calendar id", validate=lambda _, x: len(x.strip()) > 0
        )
    else:
        calendar_id = args.calendar_id

    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            api.delete_calendar(calendar_id)
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return

    print(Style.BRIGHT + Fore.GREEN + "Calendar deleted!" + Style.RESET_ALL)


def edit_calendar(api: Api, config, args):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # If one of the arguments is not None
    has_args = False
    for arg in vars(args):
        if getattr(args, arg) is not None and arg != "func" and arg != "calendar_id":
            if arg in [
                "disable_reminders",
                "disable_congrats",
                "enable_reminders",
                "enable_congrats",
                "enable",
                "disable",
            ]:
                if getattr(args, arg):
                    has_args = True
            else:
                has_args = True

    if "calendar_id" not in args or args.calendar_id is None:
        # Ask user for calendar id
        calendar_id = inquirer.text(
            message="Calendar id", validate=lambda _, x: len(x.strip()) > 0
        )
    else:
        calendar_id = args.calendar_id

    # Get existing calendar
    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            calendar = api.get_calendar(calendar_id)
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return

    # Set default values
    default_notifications = []
    if calendar["notifications"]["reminders"]:
        default_notifications.append("Reminders")
    if calendar["notifications"]["congrats"]:
        default_notifications.append("Congratulations")
    notifications = default_notifications

    default_agenda = [days[x] for x in range(len(days)) if calendar["agenda"][x]]

    # If no arguments are specified, ask user for informations
    if not has_args:
        # Calendar name
        name = inquirer.text(
            message="Calendar name",
            default=calendar["name"],
            validate=lambda _, x: len(x.strip()) > 0,
        )
        # Ask if user wants to enable notifications
        default_notifications = []
        if calendar["notifications"]["reminders"]:
            default_notifications.append("Reminders")
        if calendar["notifications"]["congrats"]:
            default_notifications.append("Congratulations")
        notifications = inquirer.checkbox(
            message="Enable notifications?",
            choices=["Reminders", "Congratulations"],
            default=default_notifications,
        )
        # Ask for the agenda
        agenda = inquirer.checkbox(
            message="Agenda (disabled days will be frozen)",
            choices=days,
            default=default_agenda,
        )
        # Ask if the calendar should be enabled
        enabled = inquirer.confirm(
            message="Enable calendar?", default=calendar["enabled"]
        )
    # If arguments are specified, and there is a name, check the arguments
    else:
        name = calendar["name"]
        if "name" in args and args.name is not None and args.name.strip() != "":
            name = args.name

        # Check that there is not both disable and enable
        if (
            "disable_reminders" in args
            and args.disable_reminders
            and "enable_reminders" in args
            and args.enable_reminders
        ):
            print(
                Style.BRIGHT
                + Fore.RED
                + "You cannot both enable and disable reminders!"
                + Style.RESET_ALL
            )
            return
        if (
            "disable_congrats" in args
            and args.disable_congrats
            and "enable_congrats" in args
            and args.enable_congrats
        ):
            print(
                Style.BRIGHT
                + Fore.RED
                + "You cannot both enable and disable congratulations!"
                + Style.RESET_ALL
            )
            return

        if "disable_reminders" in args and args.disable_reminders:
            notifications.remove("Reminders")
        if "disable_congrats" in args and args.disable_congrats:
            notifications.remove("Congratulations")
        if "enable_reminders" in args and args.enable_reminders:
            notifications.append("Reminders")
        if "enable_congrats" in args and args.enable_congrats:
            notifications.append("Congratulations")

        agenda = default_agenda
        if "agenda" in args and args.agenda is not None:
            agenda = []
            for day in args.agenda.split(","):
                day = day.strip().capitalize()
                if day in days:
                    agenda.append(day)
                else:
                    print(
                        Style.BRIGHT
                        + Fore.RED
                        + "Invalid day: "
                        + day
                        + Style.RESET_ALL
                    )
                    return

        enabled = calendar["enabled"]
        if "enable" in args and args.enable:
            enabled = True
        if "disable" in args and args.disable:
            enabled = False

    edited_calendar = {
        "name": name.strip(),
        "agenda": [day in agenda for day in days],
        "notifications": {
            "reminders": "Reminders" in notifications,
            "congrats": "Congratulations" in notifications,
        },
        "enabled": enabled,
    }

    with status.Status("", spinner="point", spinner_style="blue"):
        api.edit_calendar(calendar_id, edited_calendar)
    print(Style.BRIGHT + Fore.GREEN + "Calendar updated!" + Style.RESET_ALL)
