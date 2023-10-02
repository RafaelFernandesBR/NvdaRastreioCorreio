import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError  # Importe a classe HTTPError


class RequestCorreios:
	# track an order, with the tracking code.
	def get_tracking(self, code):
		url = f"http://androidparacegos.com.br/rastrear/{code}"
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
		}
		request = Request(url, headers=headers)

		try:
			response = urlopen(request)
			events = json.loads(response.read().decode('utf-8'))

			return events
		except HTTPError as e:
			if e.code == 400:
				error_message = json.loads(e.read().decode('utf-8'))
				raise ValueError(error_message['mensagem'])
