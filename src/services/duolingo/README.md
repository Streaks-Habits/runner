# 🦜 Duolingo

Will expand the streak if you have reached your daily goal on Duolingo.

## Credentials

You need to provide your Duolingo username and password via the `DUOLINGO_USERNAME` and `DUOLINGO_PASSWORD` environment variables, or via a `.env` file at the root of the project.

```env
DUOLINGO_USERNAME=<your username>
DUOLINGO_PASSWORD=<your password>
```

## Example
```yml
instance: "https://streaks.chevro.fr"
api_key: "your_api_key"
services:
- type: duolingo
  name: "🦜 Duolingo"
  enable: true
  goal: 15xp
  calendars:
  - '63c028aa405c3470bac95040'
```

## Configuration

### **type**

The type of the service. It must be `duolingo`.

### **name**

The name of the service. Choose anything you want.

### **enable**

Whether the service is enabled or not. It must be `true` or `false`.

### **goal**

The goal is the number of XP you want to reach every day. It must be a number followed by the letters `xp`, like `15xp` or `50xp`.

To disable the goal, remove the `goal` line from your configuration or set it to `0xp`.

### **calendars**

A list of calendars IDs for the calendars that will see their streaks expanded when you reach your goal.