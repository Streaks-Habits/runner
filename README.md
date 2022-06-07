![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Gitlab pipeline status (self-hosted)](https://img.shields.io/gitlab/pipeline-status/streaks/runner?branch=main&gitlab_url=https%3A%2F%2Fgit.chevro.fr&style=flat-square)
![Maintenance](https://img.shields.io/maintenance/yes/2022?style=flat-square)

<img src="src/brand/logo.svg" height="60" width="60" align="right">

Streaks Runner
==============

Streaks Runner, to automate the completion of your tasks on the streaks habit tracking application.

This runner will fetch data from third party services to verify that you have followed your habit and enter it on your dashboard.

Installation
============

With Docker (recommended)
-------------------------
Download the `docker-compose.yml` and a sample `config.yml`
```bash
mkdir streaks-runner && cd "$_"
wget https://git.chevro.fr/streaks/runner/-/raw/main/docker-compose.yml
wget https://git.chevro.fr/streaks/runner/-/raw/main/config.example.yml -O config.yml
```

**Go to the [Configuration](#configuration) section to edit your `config.yml` file, then come back here.**

Start your container with:
```bash
docker-compose up -d
```

You can check that everything went well by looking at the container logs:
```bash
docker-compose logs
```

Or by looking at the daemon logs:
```bash
cat logs/daemons.log
```

Manual install
--------------
Officially supported on Linux, may work on another platform.

Install the following dependencies on your server:
- NodeJS (with npm)
- Python v3 (with pip)

Clone the repository:
```bash
git clone https://git.chevro.fr/streaks/runner.git streaks-runner && cd streaks-runner
```

You can now install the runner dependencies:
```bash
npm i
pip3 install -r daemons/requirements.txt
```

**Go to the [Configuration](#configuration) section to edit your `config.yml` file, then come back here.**

Build and start the server with:
```bash
npm run build
npm run start
```

You can check that everything went well by looking at the daemons logs:
```bash
cat logs/daemons.log
```

Configuration
=============

⚠️ Some daemons ask you for your credentials to third party services. In these cases you need to be very careful with your `config.yml` file. ⚠️

----

The minimal `config.yml` file should look like this:
```yml
instance: "https://streaks.chevro.fr"
api_key: "you_api_key"
cron: "50 * * * *"
services:
  <The services configuration (detailed below)>
```

### **instance**

This is the address of the Streaks instance you are using.

### **api_key**
This is your Streaks API key, these are generated from the Streaks application and allow the runner to mark your successes.

### **cron**
The cron syntax is used to know when the runner should go and make requests to the third party service to know if you have done your habit. The default cron is "50 * * * *", which means every hour, at minute 50.
You can view your cron on the website <a href="https://crontab.guru/#50_*_*_*_*" target="_blank">https://crontab.guru</a>

### **services**
The services section includes the configuration of each third party service you will use. The syntax will look like :
```yml
services:
  duolingo:
    enable: true
    calendar: "your_calendar_id"
    username: "your_duolingo_login"
    password: "you_duolingo_password"
  <other service>:
	<other fields>: <value>
```

But each service requires a different configuration and is listed in the [Supported services](#supported-services) section.

Supported services
==================

Here is a list of supported services, each service has its own README which contains its configuration instructions for the `config.yml` file.

- [Duolingo](daemons/duolingo/)
- [Intra 42](daemons/intra42/)
