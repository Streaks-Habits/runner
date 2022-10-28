# Duolingo runner

This daemon verifies that you have practiced a language on duolingo this day.

If you have completed at least one activity on duolingo, your streaks will be validated.

## Configuration

```yml
services:
  duolingo:
    enable: true
    calendar: "your_calendar_id"
    username: "your_duolingo_login"
    password: "your_duolingo_password"
    goal: "streak|[num]xp" # e.g. "streaks" or "xp" or "55xp" or "100xp"...
```

### Goal Types

- **streak**

  The streak type validates your day if you have expanded your Duolingo streaks.
- **xp**

  The xp type validates your day if you have reached your xp goal for the day on Duolingo. The xp goal come from your Duolingo's settings.
- **[num]xp**

  The xp type validates your day if you have reached the given xp goal for the day on Duolingo.

  *e.g. 25xp, 100xp*

## Testing

You can test the daemon in this way:

```bash
python main.py '{"username": "<username>", "password": "<password>", "goal": "<streak|[num]xp>"}'
```
