import { load } from 'js-yaml'
import fs from 'fs'

export interface Config {
	instance: string,
	api_key: string,
	cron: string,
	services: {
		duolingo: {
			enable: boolean,
			calendar: string,
			username: string,
			password: string
		},
		intra42: {
			enable: boolean,
			calendar: string,
			username: string,
			password: string
		}
	}
}

const file = fs.readFileSync('./config.yml', 'utf8')
export const conf: Config = load(file) as Config

export const emptyConf: Config = {
	instance: "",
	api_key: "",
	cron: "",
	services: {
		duolingo: {
			enable: false,
			calendar: "",
			username: "",
			password: ""
		},
		intra42: {
			enable: false,
			calendar: "",
			username: "",
			password: ""
		}
	}
}
