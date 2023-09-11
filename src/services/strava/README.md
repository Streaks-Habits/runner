# 🚴 Strava

Will expand the streak if you have made an activity on Strava. You can also specify the type of activity or / and the minimum distance.

## Credentials

Go to <https://www.strava.com/settings/api> and create an application.

Then, provide your Strava application credentials via environment variables, or via a `.env` file at the root of the project.

```env
STRAVA_APP_CLIENT_ID=<app_client_id>
STRAVA_APP_CLIENT_SECRET=<app_client_secret>
STRAVA_APP_REFRESH_TOKEN=<app_refresh_token>
```

### Authentication

You will need to authenticate your Strava account to the application. To do so, run the following command:

```bash
python src/services/strava/main.py
```

The script will write a `STRAVA_ACCESS_TOKEN`  and a `STRAVA_REFRESH_TOKEN` environment variable in your `.env` file.

## Example
```yml
instance: "https://streaks.chevro.fr"
api_key: "your_api_key"
services:
- type: strava
  name: "🚴 Strava"
  enable: true
  activities:
    - 'Run'
    - 'VirtualRun'
  validation_measure: '5' # (km) Optional
  calendars:
  - '63c028aa405c3470bac95040'
```

## Configuration

### **type**

The type of the service. It must be `gitlab`.

### **name**

The name of the service. Choose anything you want.

### **enable**

Whether the service is enabled or not. It must be `true` or `false`.

### **activities**

The list of activities that will trigger the streak expansion.

Possible values are:
- `All`
- `AlpineSki`
- `BackcountrySki`
- `Canoeing`
- `Crossfit`
- `EBikeRide`
- `Elliptical`
- `EMountainBikeRide`
- `Golf`
- `GravelRide`
- `Handcycle`
- `Hike`
- `IceSkate`
- `InlineSkate`
- `Kayaking`
- `Kitesurf`
- `MountainBikeRide`
- `NordicSki`
- `Ride`
- `RockClimbing`
- `RollerSki`
- `Rowing`
- `Run`
- `Sail`
- `Skateboard`
- `Snowboard`
- `Snowshoe`
- `Soccer`
- `StairStepper`
- `StandUpPaddling`
- `Surfing`
- `Swim`
- `TrailRun`
- `Velomobile`
- `VirtualRide`
- `VirtualRun`
- `Walk`
- `WeightTraining`
- `Wheelchair`
- `Windsurf`
- `Workout`
- `Yoga`

### **validation_measure**

The minimum distance of the activity to trigger the streak expansion. It must be a number.

### **calendars**

A list of calendars IDs for the calendars that will see their streaks expanded when you reach your goal.
