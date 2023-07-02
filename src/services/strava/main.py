import requests
import dateparser
from datetime import date, datetime

from services.strava.api import (
    ATHLETE_ACTIVITIES_ENDPOINT,
    refresh_and_get_access_token,
)


# Return an array of activities between today and 'after'
# https://developers.strava.com/docs/reference/#api-models-SummaryActivity
def _get_activities(access_token, after=date.today(), per_page=30):
    if per_page > 200:
        per_page = 200

    after_datetime = datetime.combine(after, datetime.min.time())
    after_timestamp = after_datetime.timestamp()

    activities = []
    page = 1
    while True:
        # Get activities
        resp = requests.get(
            f"{ATHLETE_ACTIVITIES_ENDPOINT}?page={page}&per_page={per_page}&after={after_timestamp}",
            headers={"Authorization": "Bearer " + access_token},
        )
        if resp.status_code == 200:
            if len(resp.json()) == 0:
                break
            activities += resp.json()
        else:
            print(resp.status_code)
            print(resp.text)
            break
        page += 1

    return activities


# Return an array of activities
# Each activity is a dict with the following
# {
# 'date': str,
# 'measure': str (distance in km)
# }
def get_activities(access_token, after=date.today(), per_page=30):
    raw_activities = _get_activities(access_token, after, per_page)
    activities = []
    for activity in raw_activities:
        activities.append(
            {
                "date": dateparser.parse(activity["start_date_local"]),
                "type": activity["sport_type"],
                "measure": str(activity["distance"] / 1000),
            }
        )
    return activities


# Will return at least num_data activities
def get_data(settings, after=date.today()):
    access_token = refresh_and_get_access_token()

    return get_activities(access_token, after, 200)


def is_success(settings, day):
    if not day:
        return False
    # Check if the activity type is in the list of activities
    if (
        day["type"] not in settings["activities"]
        and len(settings["activities"]) > 0
        and "All" not in settings["activities"]
    ):
        return False
    # Check if there is a validation measure
    if "validation_measure" not in settings:
        return True
    # If there is a validation measure,
    # check if the measure is greater than the validation measure
    if float(day["measure"]) >= float(settings["validation_measure"]):
        return True
    return False


# TODO: check settings function to run before all
