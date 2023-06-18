import requests
import re
from pathlib import Path
import dotenv
import os

URL = "https://brilliant.org/home/"

dotenv_file = Path(".env")
dotenv_file.touch(exist_ok=True)
dotenv.load_dotenv(dotenv_file)

if not os.getenv("BRILLIANT_SESSION_ID"):
    raise Exception("Brilliant: Missing 'BRILLIANT_SESSION_ID' in ENV")

# Fetch home page with session cookie
resp = requests.get(
    URL, cookies={"sessionid": os.getenv("BRILLIANT_SESSION_ID", "")}
)
# Extract the "calendar":[] array from the page
m = re.search(r'calendar":(\[.*?\]),', resp.text)
if not m:
    # User is not logged in
    raise Exception("Brilliant: Invalid session ID")

calendar = m.group(1)
# Parse the JSON
calendar = calendar.replace("true", "True").replace("false", "False")
calendar = eval(calendar)

# Loop through the calendar
for day in calendar:
    if day["current_day"]:
        print(f"Today is {day['highlighted']}")
        break
