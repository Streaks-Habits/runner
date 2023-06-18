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
        [
            len(f"{prog['current_progress']}/{prog['goal']}")
            for prog in progresses
        ]
    )

    for prog in progresses:
        print(Fore.BLUE + prog["_id"] + Style.RESET_ALL + " ", end="")

        if prog["current_progress"] >= prog["goal"]:
            print(Fore.GREEN, end="")
        else:
            print(Fore.RED, end="")

        print(
            f"{prog['current_progress']}/{prog['goal']}".ljust(max_len, " ")
            + " ",
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
    # Ask user for informations
    # Progress name
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

    new_progress = {
        "name": name.strip(),
        "goal": int(goal),
        "recurrence_unit": recurrence_unit,
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
