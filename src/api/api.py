import requests
from api.exceptions import NotFoundException


class Api:
    api_key: str = ""
    instance: str = ""
    user_id: str = ""

    def __init__(self, api_key: str, instance: str):
        self.api_key = api_key
        self.instance = instance
        self.user_id = self.api_key.split(":")[0]

    def _request(self, method: str, endpoint: str, data: dict = {}):
        resp = requests.request(
            method,
            f"{self.instance}{endpoint}",
            headers={"x-api-key": self.api_key},
            json=data,
        )
        if resp.status_code == 404:
            raise NotFoundException(resp.json()["message"])
        if resp.status_code != 200 and resp.status_code != 201:
            raise Exception(resp.text)
        return resp.json()

    def get_calendars(self):
        return self._request("GET", "/api/v1/calendars/user/" + self.user_id)

    def get_progresses(self):
        return self._request("GET", "/api/v1/progresses/user/" + self.user_id)

    def set_calendar_state(self, calendar_id: str, state: str, for_date: str):
        return self._request(
            "POST",
            f"/api/v1/calendars/state/{calendar_id}/{state}?for={for_date}",
        )

    def create_calendar(self, new_calendar: dict):
        new_calendar["user"] = self.user_id
        return self._request("POST", "/api/v1/calendars", new_calendar)

    def create_progress(self, new_progress: dict):
        new_progress["user"] = self.user_id
        return self._request("POST", "/api/v1/progresses", new_progress)

    def delete_calendar(self, calendar_id: str):
        return self._request("DELETE", "/api/v1/calendars/" + calendar_id)

    def delete_progress(self, progress_id: str):
        return self._request("DELETE", "/api/v1/progresses/" + progress_id)

    def get_calendar(self, calendar_id: str):
        return self._request("GET", "/api/v1/calendars/" + calendar_id)

    def get_progress(self, progress_id: str):
        return self._request("GET", "/api/v1/progresses/" + progress_id)

    def edit_calendar(self, calendar_id: str, new_calendar: dict):
        return self._request(
            "PUT", "/api/v1/calendars/" + calendar_id, new_calendar
        )

    def edit_progress(self, progress_id: str, new_progress: dict):
        return self._request(
            "PUT", "/api/v1/progresses/" + progress_id, new_progress
        )
