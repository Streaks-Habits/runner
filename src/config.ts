import { load } from 'js-yaml'
import fs from 'fs'

export interface IConfig {
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
		gitlab: {
			enable: boolean,
			calendar: string,
			instance: string,
			username: string
		},
		intra42: {
			enable: boolean,
			calendar: string,
			username: string,
			password: string
		},
		strava: {
			enable: boolean,
			calendar: string,
			athlete_id: string,
			activities: Array<string>
		}
	}
}

export type TServices = IConfig['services']['duolingo'] |
						IConfig['services']['gitlab'] |
						IConfig['services']['intra42'] |
						IConfig['services']['strava']

const file = fs.readFileSync('./config.yml', 'utf8')
export const conf: IConfig = load(file) as IConfig

export const emptyConf: IConfig = {
	instance: '',
	api_key: '',
	cron: '',
	services: {
		duolingo: {
			enable: false,
			calendar: '',
			username: '',
			password: ''
		},
		gitlab: {
			enable: false,
			calendar: '',
			instance: '',
			username: ''
		},
		intra42: {
			enable: false,
			calendar: '',
			username: '',
			password: ''
		},
		strava: {
			enable: false,
			calendar: '',
			athlete_id: '',
			activities: []
		}
	}
}
