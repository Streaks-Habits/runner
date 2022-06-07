Duolingo runner
===============

This daemon verifies that you have practiced a language on duolingo this day.

If you have completed at least one activity on duolingo, your streaks will be validated.

Configuration
=============
```yml
services:
  duolingo:
    enable: true
    calendar: "your_calendar_id"
    username: "your_duolingo_login"
    password: "your_duolingo_password"
```

Testing
-------
You can test the daemon in this way:
```bash
python main.py <login> <password>
```
