import requests
from pathlib import Path
import dotenv
import os
import dateparser
from datetime import date, timedelta

URL = "https://git.chevro.fr/"

dotenv_file = Path(".env")
dotenv_file.touch(exist_ok=True)
dotenv.load_dotenv(dotenv_file)


def req(url):
    resp = requests.get(
        url, headers={"Authorization": f"Bearer {os.getenv('GITLAB_TOKEN')}"}
    )
    if resp.status_code != 200:
        raise Exception("GitLab: Invalid token")
    return resp.json()


def get_events(after=date.today(), per_page=20):
    if per_page > 100:
        per_page = 100

    # after = yesterday
    after = after - timedelta(days=1)

    # Fetch user events
    events = []
    page = 1
    while True:
        api_avents = req(
            f"{URL}/api/v4/events?after={after}&page={page}&per_page={per_page}"
        )
        if len(api_avents) == 0:
            break

        for api_event in api_avents:
            # Get project info
            project = req(f"{URL}/api/v4/projects/{api_event['project_id']}")
            events.append(
                {
                    "date": dateparser.parse(api_event["created_at"]),
                    "action": api_event["action_name"],
                    "project": project["name"],
                    "project_id": project["id"],
                    "project_visibility": project["visibility"],
                }
            )
        page += 1

    return events


def get_data(settings, after=date.today()):
    return get_events(after, 100)


def is_success(settings, day):
    if not day:
        return False
    # Check if the visibility is correct (ignore if not set)
    if (
        "project_visibility" in settings
        and settings["project_visibility"] != day["project_visibility"]
    ):
        return False
    # Check if the action is in the list of actions
    if "actions" in settings:
        if (
            day["action"] not in settings["actions"]
            and len(settings["actions"]) > 0
            and "All" not in settings["actions"]
        ):
            return False
    return True
