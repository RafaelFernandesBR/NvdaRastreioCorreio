import globalPluginHandler
import ui
import urllib.request
import urllib.parse
import api
import json

def GetRastreio(code):
        url ="https://proxyapp.correios.com.br/v1/sro-rastro/{}".format(code)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 tSafari/537.36'}
        res = urllib.request.Request(url)
        res.add_header('user-agent', 'M	ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')
        content = urllib.request.urlopen(res)
        content=json.load(content)
        return content

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_obterUltimoEvento(self, gesture):
        clipboardText = api.getClipData()
        send=GetRastreio(clipboardText)
#Formatar a data em pt-BR
        dtHrCriado=send['objetos'][0]['eventos'][0]['dtHrCriado']
        dtHrCriado=dtHrCriado[8:10]+'/'+dtHrCriado[5:7]+'/'+dtHrCriado[0:4]+' '+dtHrCriado[11:13]+':'+dtHrCriado[14:16]

        msgText='{}, em {} {}, {}. Data: {}'.format(send['objetos'][0]['eventos'][0]['descricao'], send['objetos'][0]['eventos'][0]['unidade']['endereco']['cidade'], send['objetos'][0]['eventos'][0]['unidade']['endereco']['uf'], send['objetos'][0]['eventos'][0]['unidade']['tipo'], dtHrCriado)

        ui.message(str(msgText))

    def script_TodosEventos(self, gesture):
        clipboardText = api.getClipData()
        send=GetRastreio(clipboardText)
#percorrer todos os eventos
        for i in range(len(send['objetos'][0]['eventos'])):
#Formatar a data em pt-BR
            dtHrCriado=send['objetos'][0]['eventos'][i]['dtHrCriado']
            dtHrCriado=dtHrCriado[8:10]+'/'+dtHrCriado[5:7]+'/'+dtHrCriado[0:4]+' '+dtHrCriado[11:13]+':'+dtHrCriado[14:16]

            msgText='{}, em {} {}, {}. Data: {}'.format(send['objetos'][0]['eventos'][i]['descricao'], send['objetos'][0]['eventos'][i]['unidade']['endereco']['cidade'], send['objetos'][0]['eventos'][i]['unidade']['endereco']['uf'], send['objetos'][0]['eventos'][i]['unidade']['tipo'], dtHrCriado)
            ui.message(str(msgText))


    __gestures={
        "kb:nvda+e": "obterUltimoEvento",
        "kb:nvda+control+e": "TodosEventos"
    }
