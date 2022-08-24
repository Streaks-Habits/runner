Gitlab runner
=============

This daemon checks that you have made a push on Gitlab this day.

If you have made at least un push on Gitlab, your streaks will be validated.

Configuration
=============
```yml
services:
  gitlab:
    enable: false
    calendar: "your_calendar_id"
    instance: "https://gitlab.example.com"
    username: "your_gitlab_username"
```

Testing
=======
You can test the daemon in this way:
```bash
python main.py '{"instance": "<instance>", "username": "<username>"}'
```
