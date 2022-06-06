import schedule from 'node-schedule'
import chalk from 'chalk'

import { conf } from './config'
import { runDaemons } from './daemons'

///// CHECK config.yml /////
if (conf.cron == undefined || conf.cron == "") {
	console.log(chalk.red("Please add a cron in your config.yml"))
	process.exit(1)
}

schedule.scheduleJob(conf.cron, runDaemons)

console.log(`${chalk.blue("streaks runner")} => started with '${chalk.green(conf.cron)}'`)
runDaemons()
