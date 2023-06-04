import requests
import dotenv
import os
from pathlib import Path
from datetime import date, datetime
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

URL = 'https://duolingo.com/'
USER_INFOS_URL = 'https://www.duolingo.com/api/1/users/show?username='
SESSION_FILE = Path('store/duolingo_session.pickle')

dotenv_file = Path('.env')
dotenv_file.touch(exist_ok=True)
dotenv.load_dotenv(dotenv_file)

def login():
	# Create virtual display
	# display = Display(visible=0, size=(1920, 1080))
	# display.start()
	# Login to duolingo with selenium
	options = webdriver.ChromeOptions()
	# disable extensions
	options.add_argument("--disable-extensions")
	options.add_argument("--headless=new")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-dev-shm-usage")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	driver = webdriver.Chrome(options=options)
	driver.set_window_size(1920, 1080)

	stealth(driver,
		languages=["en-US", "en"],
		vendor="Google Inc.",
		platform="Win32",
		webgl_vendor="Intel Inc.",
		renderer="Intel Iris OpenGL Engine",
		fix_hairline=True,
	)

	driver.get(URL)

	# Click "I already have an account" button
	login_popup_button = driver.find_element(by=By.CSS_SELECTOR, value="button[data-test='have-account']")
	login_popup_button.click()
	# Fill username
	username_input = driver.find_element(by=By.CSS_SELECTOR, value="input[data-test='email-input']")
	username_input.send_keys(os.getenv('DUOLINGO_USERNAME'))
	# Fill password
	password_input = driver.find_element(by=By.CSS_SELECTOR, value="input[data-test='password-input']")
	password_input.send_keys(os.getenv('DUOLINGO_PASSWORD'))
	# Click "Log in" button
	login_button = driver.find_element(by=By.CSS_SELECTOR, value="button[data-test='register-button']")
	login_button.click()

	# Wait for login (check if the "Login button" is still here)
	def wait_for_login(driver):
		try:
			driver.find_element(by=By.CSS_SELECTOR, value="button[data-test='register-button']")
			return False
		except:
			return True
	wait = WebDriverWait(driver, 10)
	wait.until(wait_for_login)

	# Create store folder if not exists
	Path(Path(SESSION_FILE).parent).mkdir(parents=True, exist_ok=True)
	# Save session
	with open(SESSION_FILE, 'wb') as f:
		session_data = {
			'cookies': driver.get_cookies(),
		}
		pickle.dump(session_data, f)

def user_info_if_logged():
	# Check if session is stored
	if not os.path.isfile(SESSION_FILE):
		return False
	# Check if session is still valid
	cookies = pickle.load(open(SESSION_FILE, "rb"))['cookies']
	session = requests.Session()
	for cookie in cookies:
		session.cookies.set(cookie['name'], cookie['value'])
	try:
		response = session.get(
			USER_INFOS_URL + os.getenv('DUOLINGO_USERNAME'),
			headers={
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1474.0',
			},
		)
		if response.status_code != 200:
			return False
		user_info = response.json()
	except:
		return False
	return user_info

def get_activities(after=date.today()):

	user_info = user_info_if_logged()
	if not user_info:
		login()
		user_info = user_info_if_logged()

	activities = []
	for activity in user_info['calendar']:
		if activity['datetime'] > datetime.fromisoformat(after.isoformat()).timestamp() * 1000:
			activities.append({
				'date': datetime.fromtimestamp(activity['datetime'] / 1000),
				'xp': activity['improvement'],
			})
	return activities

def get_data(settings, after=date.today()):
	return get_activities(after)

def is_success(settings, day):
	if not day:
		return False
	if settings['goal'].endswith('xp'):
		xp_goal = int(settings['goal'].replace('xp', ''))
		return day['xp'] >= xp_goal
	return True
