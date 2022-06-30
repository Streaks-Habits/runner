Strava runner
=============

This daemon checks that you have done your sport of the day.

If you have done the activities specified in the table `activities` today, your streaks will be validated.

Configuration
=============
```yml
services:
  strava:
    enable: false
    calendar: ""
    athlete_id: ""
	activities: []
```

`activities` is a table that contains the types of activities that validate your streak of the day.
**Leave activities empty to allow you to validate your streak with any activity**
The following are known types of activity (not exhaustive):
- `run`
- `workout`

**Example**: you want to do a running session and a workout session to validate your streak:
```yml
services:
  strava:
    ...
	activities: ["run", "workout"]
```

Testing
-------
You can test the daemon in this way:
```bash
python main.py '{"athlete_id": "<athlete_id>", "activities": ["<activities>"]}'
```
