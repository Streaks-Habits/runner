import dotenv
import os
from pathlib import Path
from authlib.integrations.requests_client import OAuth2Session

AUTHORIZATION_ENDPOINT = "https://www.strava.com/oauth/authorize"
TOKEN_ENDPOINT = "https://www.strava.com/oauth/token"
ATHLETE_ACTIVITIES_ENDPOINT = "https://www.strava.com/api/v3/athlete/activities"

dotenv_file = Path(".env")
dotenv_file.touch(exist_ok=True)
dotenv.load_dotenv(dotenv_file)

# https://www.strava.com/oauth/authorize
# Connect with Strava OAuth2


def get_access_token():
    client = OAuth2Session(
        os.getenv("STRAVA_APP_CLIENT_ID"),
        os.getenv("STRAVA_APP_CLIENT_SECRET"),
        scope="activity:read_all",
        redirect_uri="http://localhost",
    )

    uri, state = client.create_authorization_url(AUTHORIZATION_ENDPOINT)
    print(uri)

    response = input("Enter the full callback URL: ")

    token = client.fetch_token(
        TOKEN_ENDPOINT,
        authorization_response=response,
        client_secret=os.getenv("STRAVA_APP_CLIENT_SECRET"),
        client_id=os.getenv("STRAVA_APP_CLIENT_ID"),
    )

    return token["access_token"], token["refresh_token"]


def refresh_access_token(refresh_token):
    # Refresh token
    client = OAuth2Session(
        os.getenv("STRAVA_APP_CLIENT_ID"),
        os.getenv("STRAVA_APP_CLIENT_SECRET"),
        scope="activity:read_all",
        redirect_uri="http://localhost",
        token_endpoint=TOKEN_ENDPOINT,
    )
    token = client.refresh_token(
        TOKEN_ENDPOINT,
        refresh_token=refresh_token,
        client_id=os.getenv("STRAVA_APP_CLIENT_ID"),
        client_secret=os.getenv("STRAVA_APP_CLIENT_SECRET"),
    )
    return token["access_token"], token["refresh_token"]


def refresh_and_get_access_token():
    # Check that STRAVA_ACCESS_TOKEN and STRAVA_REFRESH_TOKEN are set
    access_token = ""
    refresh_token = ""
    if not os.getenv("STRAVA_ACCESS_TOKEN") or not os.getenv("STRAVA_REFRESH_TOKEN"):
        access_token, refresh_token = get_access_token()
    else:
        access_token, refresh_token = refresh_access_token(
            os.getenv("STRAVA_REFRESH_TOKEN")
        )
    dotenv.set_key(dotenv_file, "STRAVA_ACCESS_TOKEN", access_token)
    dotenv.set_key(dotenv_file, "STRAVA_REFRESH_TOKEN", refresh_token)
    return access_token

if __name__ == "__main__":
	refresh_and_get_access_token()
