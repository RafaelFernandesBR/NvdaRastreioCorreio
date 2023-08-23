import globalPluginHandler
from scriptHandler import script
import ui
import api
from . import requestCorreios as RequestCorreios


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "RastreioCorreios"

	@script(
		# Gets the last event of a trace code.
		description="Obtém o último evento de um código de rastreio.",
		gestures=["kb:nvda+e"]
	)
	def script_Gets_The_Last_Event(self, gesture):
		request = RequestCorreios.RequestCorreios()
		clipboardCode = api.getClipData()
		tracking = request.get_tracking(clipboardCode)
		evento = tracking['eventos'][0]
		if not evento:
			# If events are not returned in the api.
			ui.message("Não foi possível obter os dados da API")
			return

		Date_And_Time = f"{evento['data']} {evento['hora']}"
		substatus_text = ", ".join(evento['subStatus'])
		Complete_Text = f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {Date_And_Time}"
		ui.message(Complete_Text)

	@script(
		# Gets all events for a trace code.
		description="Obtém todos os eventos de um código de rastreio.",
		gestures=["kb:nvda+control+e"]
	)
	def script_Gets_The_All_Event(self, gesture):
		request = RequestCorreios.RequestCorreios()
		clipboardCode = api.getClipData()
		tracking = request.get_tracking(clipboardCode)
		events = f"Código: {clipboardCode}\n"

		# loop through the events, and add them all to a string.
		for evento in tracking['eventos']:
			Date_And_Time = f"{evento['data']} {evento['hora']}"
			substatus_text = ", ".join(evento['subStatus'])
			events += f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {Date_And_Time}\n"

		ui.browseableMessage(events, title="Eventos rastreio")
