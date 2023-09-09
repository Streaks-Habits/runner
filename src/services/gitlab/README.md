# 🦊 GitLab

Will expand the streak if you have committed at least once today.

## Credentials

You need to provide your GitLab access token via the `GITLAB_TOKEN` environment variables, or via a `.env` file at the root of the project.

```env
GITLAB_TOKEN=<your_token>
```

## Example
```yml
instance: "https://streaks.chevro.fr"
api_key: "your_api_key"
services:
- type: gitlab
  name: "🦊 GitLab"
  enable: true
  project_visibility: 'public'
  actions:
  - 'pushed_to'
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

### **project_visibility**

The visibility of the projects to consider.

Possible values are:
- `public`
- *TODO: add the list of possible values.*

### **actions**

A list of actions that will trigger the streak expansion.

Possible values are:
- `All`
- `pushed_to`
- *TODO: add the list of possible values.*

### **calendars**

A list of calendars IDs for the calendars that will see their streaks expanded when you reach your goal.
