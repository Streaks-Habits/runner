import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'
import os from 'os'
import chalk from 'chalk'
import moment from "moment"

import { conf, emptyConf, Config } from './config'
import { capitalize } from './utils'
import { getCli } from './services'

function checkConfig(serviceName: string, service: Object, emptyService: Object): boolean {
	let serviceKeys = Object.keys(service)
	let emptyServiceKeys = Object.keys(emptyService)
	let hasProblem = false

	emptyServiceKeys.forEach((key) => {
		if (!serviceKeys.includes(key)) {
			console.log(chalk.red(`${chalk.bold(serviceName)}: ${key} missing.`))
			hasProblem = true
		}
	})

	serviceKeys.forEach((key) => {
		if (!emptyServiceKeys.includes(key)) {
			console.log(chalk.red(`${chalk.bold(serviceName)}: ${key} property isn't supported.`))
			hasProblem = true
		}
	})

	return !hasProblem
}

function getExecPromise(conf: Config, servConf: any, serviceName: string, command: string): Promise<void> {
	const logPath: string = path.resolve("log", "daemons.log")
	const startDate: Date = new Date()

	return new Promise((resolve, reject) => {
		exec(command, (error, stdout, stderr) => {
			var errorString: string = ''

			// Get error string if there's error
			if (error)
				errorString = `error: ${error.message}`
			else if (stderr)
				errorString = `command error: ${stderr}`
			else if (stdout.trim() && stdout.trim() != "success")
				errorString = `output: ${stdout}`
			if (errorString != '')
				errorString = `${startDate.toISOString()} => ${serviceName} : ${errorString.trim()}${os.EOL}`

			if (errorString == '' && stdout.trim() == "success") {
				// Call API if there's no errors and the program returns a success
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
			else if (errorString != '') {
				// Log error message on error
				fs.appendFile(logPath, errorString, 'utf-8', (err) => {
					if (err) console.log(chalk.red(err))

					resolve()
				})
			}
			else {
				// If a daemons has no error but return something else than an error
				resolve()
			}
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

		Object.keys(conf.services).forEach(name => {
			// Check that the service exists in config
			if (!Object.keys(emptyConf.services).includes(name))
				return console.log(chalk.red(`${chalk.bold(name)} is not a supported service.`))

			const service = conf.services[name as keyof typeof conf.services]
			const emptyService = emptyConf.services[name as keyof typeof emptyConf.services]

			if (!checkConfig(capitalize(name), service, emptyService))
				return

			console.log(`Starting ${chalk.cyan(capitalize(name))}...`)
			const cli = getCli(name).replace("<DATA>", JSON.stringify(service))
			execPromises.push(getExecPromise(conf, service, name, cli))
		})

		Promise.allSettled(execPromises).then(() => {
			console.log("✅ Done.")
			resolve()
		})
	})
}
