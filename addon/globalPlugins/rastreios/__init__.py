import globalPluginHandler
from scriptHandler import script
import ui
import api
import json
from . import requestCorreios as RequestCorreios


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "RastreioCorreios"

    @script(
        description="Obtém o último evento de um código de rastreio.",
        gestures=["kb:nvda+e"]
    )
    def script_obter_ultimo_evento(self, gesture):
        request = RequestCorreios.RequestCorreios()
        clipboard_text = api.getClipData()
        send = request.get_rastreio(clipboard_text)
        evento = send['eventos'][0]
        if not evento:
            ui.message("Não foi possível obter os dados da API")
            return

        dt_hr_criado = f"{evento['data']} {evento['hora']}"
        substatus_text = ", ".join(evento['subStatus'])
        msg_text = f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {dt_hr_criado}"
        ui.message(msg_text)

    @script(
        description="Obtém todos os eventos de um código de rastreio.",
        gestures=["kb:nvda+control+e"]
    )
    def script_todos_eventos(self, gesture):
        request = RequestCorreios.RequestCorreios()
        clipboard_text = api.getClipData()
        send = request.get_rastreio(clipboard_text)
        eventos = f"Código: {clipboard_text}\n"

        for evento in send['eventos']:
            dt_hr_criado = f"{evento['data']} {evento['hora']}"
            substatus_text = ", ".join(evento['subStatus'])
            eventos += f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {dt_hr_criado}\n"

        ui.browseableMessage(eventos, title="Eventos rastreio")
