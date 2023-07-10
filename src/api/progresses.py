from colorama import Fore, Style
from rich import status
import inquirer

from api.api import Api


def print_progresses(api: Api, config, args):
    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            progresses = api.get_progresses()
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return

    max_len = max(
        [len(f"{prog['current_progress']}/{prog['goal']}") for prog in progresses]
    )

    for prog in progresses:
        # calendar id color (blue if enabled, grey if disabled)
        if prog["enabled"]:
            print(Fore.BLUE, end="")
        else:
            print(Fore.LIGHTBLACK_EX, end="")
        print(prog["_id"] + Style.RESET_ALL + " ", end="")

        if prog["current_progress"] >= prog["goal"]:
            print(Fore.GREEN, end="")
        else:
            print(Fore.RED, end="")

        print(
            f"{prog['current_progress']}/{prog['goal']}".ljust(max_len, " ") + " ",
            end="",
        )
        print(Style.RESET_ALL, end="")

        print(
            Style.BRIGHT
            + prog["name"]
            + Style.RESET_ALL
            + " ("
            + prog["recurrence_unit"]
            + ")"
        )


def create_progress(api: Api, config, args):
    reccurence_units = ["daily", "weekly", "monthly", "yearly"]

    # If one of the arguments is not None
    has_args = False
    for arg in vars(args):
        if getattr(args, arg) is not None and arg != "func":
            if arg in ["enable", "disable"]:
                if getattr(args, arg):
                    has_args = True
            else:
                has_args = True

    # If no arguments are specified, ask user for informations
    if not has_args:  # Progress name
        name = inquirer.text(
            message="Progress name", validate=lambda _, x: len(x.strip()) > 0
        )
        # Ask for the goal
        goal = inquirer.text(message="Goal", validate=lambda _, x: x.isdigit())
        # Ask for the recurrence unit
        recurrence_unit = inquirer.list_input(
            message="Recurrence unit",
            choices=["daily", "weekly", "monthly", "yearly"],
            default="monthly",
        )
        # Ask if the progress should be enabled
        enabled = inquirer.confirm(message="Enable progress", default=True)
    # If arguments are specified, and there is at least a name, check the arguments
    else:
        if "name" not in args or args.name is None or len(args.name.strip()) == 0:
            print(
                Style.BRIGHT
                + Fore.RED
                + "You must specify a name for the progress"
                + Style.RESET_ALL
            )
            return
        else:
            name = args.name

        goal = 100
        if "goal" in args and args.goal is not None:
            if not args.goal.isdigit():
                print(
                    Style.BRIGHT + Fore.RED + "Goal must be a number" + Style.RESET_ALL
                )
                return
            goal = args.goal

        recurrence_unit = "monthly"
        if "unit" in args and args.unit is not None:
            if args.unit not in reccurence_units:
                print(
                    Style.BRIGHT
                    + Fore.RED
                    + "Recurrence unit must be one of the following: "
                    + ", ".join(reccurence_units)
                    + Style.RESET_ALL
                )
                return
            recurrence_unit = args.unit

        enabled = True
        if "enable" in args and args.enable:
            enabled = True
        elif "disable" in args and args.disable:
            enabled = False

    new_progress = {
        "name": name.strip(),
        "goal": int(goal),
        "recurrence_unit": recurrence_unit,
        "enabled": enabled,
    }

    with status.Status("", spinner="point", spinner_style="blue"):
        api.create_progress(new_progress)
    print(Style.BRIGHT + Fore.GREEN + "Progress created!" + Style.RESET_ALL)


def delete_progress(api: Api, config, args):
    if "progress_id" not in args or args.progress_id is None:
        # Ask user for progress id
        progress_id = inquirer.text(
            message="Progress id", validate=lambda _, x: len(x.strip()) > 0
        )
    else:
        progress_id = args.progress_id

    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            api.delete_progress(progress_id)
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return
    print(Style.BRIGHT + Fore.GREEN + "Progress deleted!" + Style.RESET_ALL)


def edit_progress(api: Api, config, args):
    reccurence_units = ["daily", "weekly", "monthly", "yearly"]

    # If one of the arguments is not None
    has_args = False
    for arg in vars(args):
        if getattr(args, arg) is not None and arg != "func" and arg != "progress_id":
            if arg in ["enable", "disable"]:
                if getattr(args, arg):
                    has_args = True
            else:
                has_args = True

    # If the progress id is specified, get it
    if "progress_id" not in args or args.progress_id is None:
        # Ask user for progress id
        progress_id = inquirer.text(
            message="Progress id", validate=lambda _, x: len(x.strip()) > 0
        )
    else:
        progress_id = args.progress_id

    # Get existing progress
    with status.Status("", spinner="point", spinner_style="blue"):
        try:
            progress = api.get_progress(progress_id)
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + str(e) + Style.RESET_ALL)
            return

    # If no arguments are specified, ask user for informations
    if not has_args:
        # Progress name
        name = inquirer.text(
            message="Progress name",
            default=progress["name"],
            validate=lambda _, x: len(x.strip()) > 0,
        )
        # Ask for the goal
        goal = inquirer.text(
            message="Goal", default=progress["goal"], validate=lambda _, x: x.isdigit()
        )
        # Ask for the recurrence unit
        recurrence_unit = inquirer.list_input(
            message="Recurrence unit",
            choices=reccurence_units,
            default=progress["recurrence_unit"],
        )
        # Ask if the progress should be enabled
        enabled = inquirer.confirm(
            message="Enable progress", default=progress["enabled"]
        )
    # If arguments are specified, and there is a name, check the arguments
    else:
        name = progress["name"]
        if "name" in args and args.name is not None and args.name.strip() != "":
            name = args.name

        goal = progress["goal"]
        if "goal" in args and args.goal is not None:
            if not args.goal.isdigit():
                print(
                    Style.BRIGHT + Fore.RED + "Goal must be a number" + Style.RESET_ALL
                )
                return
            goal = args.goal

        recurrence_unit = progress["recurrence_unit"]
        if "unit" in args and args.unit is not None:
            if args.unit not in reccurence_units:
                print(
                    Style.BRIGHT
                    + Fore.RED
                    + "Recurrence unit must be one of the following: "
                    + ", ".join(reccurence_units)
                    + Style.RESET_ALL
                )
                return
            recurrence_unit = args.unit

        enabled = progress["enabled"]
        if "enable" in args and args.enable:
            enabled = True
        elif "disable" in args and args.disable:
            enabled = False

    edited_progress = {
        "name": name.strip(),
        "goal": int(goal),
        "recurrence_unit": recurrence_unit,
        "enabled": enabled,
    }

    with status.Status("", spinner="point", spinner_style="blue"):
        api.edit_progress(progress_id, edited_progress)
    print(Style.BRIGHT + Fore.GREEN + "Progress updated!" + Style.RESET_ALL)
