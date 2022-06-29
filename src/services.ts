export function getCli(serviceName: string): string {
	serviceName = serviceName.toLowerCase()

	switch (serviceName) {
		case 'intra42':
			return `/usr/bin/python3 ./daemons/intra42/main.py '<DATA>'`
		case 'duolingo':
			return `/usr/bin/python3 ./daemons/duolingo/main.py '<DATA>'`
		default:
			return ``
	}
}
