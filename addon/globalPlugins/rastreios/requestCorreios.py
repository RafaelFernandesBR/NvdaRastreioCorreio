import json
from urllib.request import urlopen, Request


class RequestCorreios:
	# track an order, with the tracking code.
	def get_tracking(self, code):
		url = f"http://androidparacegos.com.br/rastrear/{code}"
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 tSafari/537.36'}
		request = Request(url, headers=headers)
		response = urlopen(request)
		events = json.loads(response.read().decode('utf-8'))

		if not events:
			raise ValueError("Não foi possível obter os dados da API")

		return events
