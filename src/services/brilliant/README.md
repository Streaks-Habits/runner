# ✨ Brilliant

Will expand the streak if you achieved your daily lesson on Brilliant.

## Credentials

You need to provide your Brilliant session cookie via the `BRILLIANT_SESSION` environment variable, or via a `.env` file at the root of the project.

You can use the [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension to find your session cookie.

```env
BRILLIANT_SESSION_ID=<your session id>
```

## Example
```yml
instance: "https://streaks.chevro.fr"
api_key: "your_api_key"
services:
- type: brilliant
  name: "✨ Brilliant"
  enable: true
  calendars:
  - '63c028aa405c3470bac95040'
```

## Configuration

### **type**

The type of the service. It must be `brilliant`.

### **name**

The name of the service. Choose anything you want.

### **enable**

Whether the service is enabled or not. It must be `true` or `false`.

### **calendars**

A list of calendars IDs for the calendars that will see their streaks expanded when you reach your goal.