import globalPluginHandler
from scriptHandler import script
import ui
import api
import json
from urllib.request import urlopen, Request


def get_rastreio(code):
    url = f"http://androidparacegos.com.br/rastrear/{code}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 tSafari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    data = json.loads(response.read().decode('utf-8'))

    if not data:
        raise ValueError("Não foi possível obter os dados da API")

    return data


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "RastreioCorreios"

    @script(
        description="Obtém o último evento de um código de rastreio.",
        gestures=["kb:nvda+e"]
    )
    def script_obter_ultimo_evento(self, gesture):
        clipboard_text = api.getClipData()
        send = get_rastreio(clipboard_text)
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
        clipboard_text = api.getClipData()
        send = get_rastreio(clipboard_text)
        eventos = f"Código: {clipboard_text}\n"

        for evento in send['eventos']:
            dt_hr_criado = f"{evento['data']} {evento['hora']}"
            substatus_text = ", ".join(evento['subStatus'])
            eventos += f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {dt_hr_criado}\n"

        ui.browseableMessage(eventos, title="Eventos rastreio")
