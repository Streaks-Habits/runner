import requests

class Api:
	api_key: str = ''
	instance: str = ''
	user_id: str = ''

	def __init__(self, api_key: str, instance: str):
		self.api_key = api_key
		self.instance = instance
		self.user_id = self.api_key.split(':')[0]

	def _request(self, method: str, endpoint: str, data: dict = {}):
		resp = requests.request(
			method,
			f'{self.instance}{endpoint}',
			headers={'x-api-key': self.api_key},
			json=data,
		)
		if resp.status_code != 200:
			raise Exception(resp.text)
		return resp.json()

	def get_calendars(self):
		return self._request('GET', '/api/v1/calendars/user/' + self.user_id)

	def get_progresses(self):
		return self._request('GET', '/api/v1/progresses/user/' + self.user_id)
