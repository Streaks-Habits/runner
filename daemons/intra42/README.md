# Intra 42 runner

This daemon verifies that you have worked at school that day.

If you have logged in to school for at least one minute, your streaks will be validated.

## Configuration

```yml
services:
  duolingo:
    enable: true
    calendar: "your_calendar_id"
    username: "your_duolingo_login"
    password: "your_duolingo_password"
```

## Testing

You can test the daemon in this way:

```bash
python main.py '{"username": "<username>", "password": "<password>"}'
```
