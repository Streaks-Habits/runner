# Streaks CLI

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Gitlab pipeline status (self-hosted)](https://img.shields.io/gitlab/pipeline-status/streaks/runner?branch=main&gitlab_url=https%3A%2F%2Fgit.chevro.fr&style=flat-square)
![Maintenance](https://img.shields.io/maintenance/yes/2023?style=flat-square)

<img src="src/brand/logo.svg" height="60" width="60" align="right">

Streaks CLI, to manage your calendars and progresses, ant to automate the completion of your tasks on the streaks habit tracking application.

The runners will fetch data from third party services to verify that you have followed your habit and enter it on your dashboard.

## Installation

Officially supported on Linux, may work on another platform.

1. Install the following dependencies on your server:

- Python v3 (with pip)
- pipenv (`pip install pipenv`)

2. Clone the repository:

```bash
git clone https://git.chevro.fr/streaks/cli.git
```

3. You can now install the cli dependencies:

```bash
pipenv install
```

4. Build the executable

```bash
pipenv run compile
```

**Go to the [Configuration](#configuration) section to edit your `config.yml` file, then come back here.**

## Using the CLI

### Calendars

#### List calendars

```bash
./streaks calendars list
```

## Configuration

⚠️ Some services may ask you for your credentials to third party services. In these cases you need to be very careful with your `config.yml` file. ⚠️

----

The minimal `config.yml` file should look like this:

```yml
instance: "https://streaks.chevro.fr"
api_key: "your_api_key"
services:
  <The services configuration (detailed below)>
```

### **instance**

This is the address of the Streaks instance you are using.

### **api_key**

This is your Streaks API key, these are generated from the Streaks application and allow the runner to mark your successes.

### **services**

**This is an optionnal section that you need to configure only if you want to use the runners (fetch a day status from a third-party service)**

The services section includes the configuration of each third party service you will use. The syntax will look like :

```yml
services:
- type: duolingo
  name: "🦜 Duolingo"
  enable: true
  goal: 15xp
  calendars:
  - '63c028aa405c3470bac95040'
```

But each service requires a different configuration, here is a list of the built-in services

## Built-in services

Here is a list of supported services, each service has its own README which contains its configuration instructions for the `config.yml` file.

- [Duolingo](src/services/duolingo/)
- [Strava](src/services/strava/)
- [Gitlab](src/services/gitlab/)
- [Brilliant](src/services/brilliant/)