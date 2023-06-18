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
        print(Fore.BLUE + cal["_id"] + Style.RESET_ALL + " ", end="")
        if cal["streak_expended_today"]:
            print(Fore.GREEN, end="")
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
            if arg in ["disable_reminders", "disable_congrats"]:
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
    # If arguments are specified, check that at least the name is specified
    elif "name" not in args or args.name is None:
        print(
            Style.BRIGHT
            + Fore.RED
            + "You must specify a name!"
            + Style.RESET_ALL
        )
        return
    # If arguments are specified, and there is a name, check the arguments
    else:
        if args.name.strip() == "":
            print(
                Style.BRIGHT
                + Fore.RED
                + "You must specify a name!"
                + Style.RESET_ALL
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

    new_calendar = {
        "name": name.strip(),
        "agenda": [day in agenda for day in days],
        "notifications": {
            "reminders": "Reminders" in notifications,
            "congrats": "Congratulations" in notifications,
        },
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
        if (
            getattr(args, arg) is not None
            and arg != "func"
            and arg != "calendar_id"
        ):
            if arg in [
                "disable_reminders",
                "disable_congrats",
                "enable_reminders",
                "enable_congrats",
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

    # If no arguments are specified, ask user for informations
    if not has_args:
        # Calendar name
        name = inquirer.text(
            message="Calendar name",
            default=calendar["name"],
            validate=lambda _, x: len(x.strip()) > 0,
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
    # If arguments are specified, and there is a name, check the arguments
    else:
        name = calendar["name"]
        if (
            "name" in args
            and args.name is not None
            and args.name.strip() != ""
        ):
            name = args.name

        notifications = []
        if calendar["notifications"]["reminders"]:
            notifications.append("Reminders")
        if calendar["notifications"]["congrats"]:
            notifications.append("Congratulations")

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

        agenda = [days[x] for x in range(len(days)) if calendar["agenda"][x]]
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

    edited_calendar = {
        "name": name.strip(),
        "agenda": [day in agenda for day in days],
        "notifications": {
            "reminders": "Reminders" in notifications,
            "congrats": "Congratulations" in notifications,
        },
    }

    with status.Status("", spinner="point", spinner_style="blue"):
        api.edit_calendar(calendar_id, edited_calendar)
    print(Style.BRIGHT + Fore.GREEN + "Calendar updated!" + Style.RESET_ALL)
