import json
from urllib.request import urlopen, Request
import ui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_obter_ultimo_evento(self, gesture):
        clipboard_text = api.getClipData()
        send = get_rastreio(clipboard_text)
        evento = send['eventos'][0]
        if not evento:
            ui.message("Não foi possível obter os dados da API")
            return

        dt_hr_criado = f"{evento['data']} {evento['hora']}"
        msg_text = f"{evento['status']}, em {evento['local']}. Data: {dt_hr_criado}"
        ui.message(msg_text)

    def script_todos_eventos(self, gesture):
        clipboard_text = api.getClipData()
        send = get_rastreio(clipboard_text)
        for evento in send['eventos']:
            dt_hr_criado = f"{evento['data']} {evento['hora']}"
            msg_text = f"{evento['status']}, em {evento['local']}. Data: {dt_hr_criado}"
            ui.browseableMessage(msg_text, title="Eventos rastreio")

    __gestures = {
        "kb:nvda+e": "obter_ultimo_evento",
        "kb:nvda+control+e": "todos_eventos"
    }

def get_rastreio(code):
    url = f"http://androidparacegos.com.br/rastrear/{code}"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 tSafari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    data = json.loads(response.read().decode('utf-8'))
    
    if not data:
        raise ValueError("Não foi possível obter os dados da API")
    
    return data
