export function getCli(serviceName: string): string {
	serviceName = serviceName.toLowerCase()

	switch (serviceName) {
	case 'duolingo':
		return '/usr/bin/python3 ./daemons/duolingo/main.py \'<DATA>\''
	case 'gitlab':
		return '/usr/bin/python3 ./daemons/gitlab/main.py \'<DATA>\''
	case 'intra42':
		return '/usr/bin/python3 ./daemons/intra42/main.py \'<DATA>\''
	case 'strava':
		return '/usr/bin/python3 ./daemons/strava/main.py \'<DATA>\''
	default:
		return ''
	}
}
