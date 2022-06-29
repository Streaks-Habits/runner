import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'
import os from 'os'
import chalk from 'chalk'
import moment from "moment"

import { conf, emptyConf, Config } from './config'

function checkConfig(serviceName: string, service: Object, originalService: Object): boolean {
	let serviceKeys = Object.keys(service)
	let originalServiceKeys = Object.keys(originalService)
	let hasProblem = false

	originalServiceKeys.forEach((key) => {
		if (!serviceKeys.includes(key)) {
			console.log(chalk.red(`${chalk.bold(serviceName)}: ${key} missing.`))
			hasProblem = true
		}
	})

	serviceKeys.forEach((key) => {
		if (!originalServiceKeys.includes(key)) {
			console.log(chalk.red(`${chalk.bold(serviceName)}: ${key} property isn't supported.`))
			hasProblem = true
		}
	})

	return !hasProblem
}

function getExecPromise(conf: Config, servConf: any, serviceName: string, command: string): Promise<void> {
	var logPath: string = path.resolve("log", "daemons.log")

	return new Promise((resolve, reject) => {
		exec(command, (error, stdout, stderr) => {
			var startDate: Date = new Date()
			var commandReturn: string

			if (error)
				commandReturn = `error: ${error.message}`
			else if (stderr)
				commandReturn = `command error: ${stderr}`
			else
				commandReturn = `${stdout}`
			commandReturn = `${startDate.toISOString()} => ${serviceName} : ${commandReturn.trim()}${os.EOL}`
			fs.appendFile(logPath, commandReturn, 'utf-8', (err) => {
				if (err) console.log(chalk.red(err))

				if (stdout.trim() == "success") {
					fetch(`${conf.instance}/api/set_state/${servConf.calendar}`, {
						method: "post",
						headers: {
							'Accept': 'application/json',
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({
							api_key: conf.api_key,
							date: moment().format('YYYY-MM-DD'),
							state: 'success'
						})
					})
					.then(res => {
						return res.text()
					}).then(res => {
						if (res != "OK")
							console.log(`API request: ${chalk.red(res)}`)
						resolve()
					})
				}
				else
					resolve()
			})
		})
	})
}

/**
 * Run each command in daemons/commands.list (one command per line) and put the logs in daemons/daemons.log.
 * Then run the setBreakday function
 * @returns - A promise that resolve(void) at the end
 */
export function runDaemons(): Promise<void> {
	return new Promise((resolve, _reject) => {
		var execPromises: Array<Promise<void>> = Array()

		// Check that config include the services section
		if (!Object.keys(conf).includes('services')) {
			console.log(chalk.red(`Your ${chalk.bold("config.yml")} doesn't contain the ${chalk.bold("services")} section.`))
			return resolve()
		}
		// Check that config include the instance url
		if (!Object.keys(conf).includes('instance')) {
			console.log(chalk.red(`Your ${chalk.bold("config.yml")} doesn't contain the ${chalk.bold("intance url")}.`))
			return resolve()
		}
		// Check that config include the api key
		if (!Object.keys(conf).includes('api_key')) {
			console.log(chalk.red(`Your ${chalk.bold("config.yml")} doesn't contain the ${chalk.bold("api key")}.`))
			return resolve()
		}

		Object.keys(conf.services).forEach(element => {
			// Check that the service exists in config
			if (!Object.keys(emptyConf.services).includes(element))
				return console.log(chalk.red(`${chalk.bold(element)} is not a supported service.`))

			/**** DUOLINGO ****/
			if (element == 'duolingo' && conf.services.duolingo.enable
					&& checkConfig("Duolingo", conf.services.duolingo, emptyConf.services.duolingo)) {
				console.log(`Starting 🦜 ${chalk.cyan("Duolingo")}...`)
				execPromises.push(getExecPromise(conf, conf.services.duolingo, "duolingo",
					`/usr/bin/python3 ./daemons/duolingo/main.py '${JSON.stringify(conf.services.duolingo)}'`))
			}

			/**** INTRA 42 ****/
			if (element == 'intra42' && conf.services.intra42.enable
					&& checkConfig("Intra42", conf.services.intra42, emptyConf.services.intra42)) {
				console.log(`Starting 🏫 ${chalk.cyan("Intra42")}...`)
				execPromises.push(getExecPromise(conf, conf.services.intra42, "intra42",
					`/usr/bin/python3 ./daemons/intra42/main.py '${JSON.stringify(conf.services.intra42)}'`))
			}
		})

		Promise.allSettled(execPromises).then(() => {
			console.log("✅ Done.")
			resolve()
		})
	})
}
