# -*- coding: UTF-8 -*-

import globalPluginHandler
from scriptHandler import script
import ui
import api
from . import requestCorreios as RequestCorreios
import wx
import gui


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
        try:
            tracking = request.get_tracking(clipboardCode)

            if tracking['quantidade'] == 0:
                # If events are not returned in the api.
                ui.message(
                    "Não foi possível obter os dados do código informado. Se a remeça foi enviada recentimente, aguarde até 24 horas e tente novamente!")
                return

            evento = tracking['eventos'][0]

            Date_And_Time = f"{evento['data']} {evento['hora']}"
            subsubstatus_text = ", ".join(evento['subStatus'])
            Complete_Text = f"{evento['status']}, em {evento['local']}, {substatus_text}. Data: {Date_And_Time}"
            ui.message(Complete_Text)
        except Exception as e:
            ui.message(str(e))

    @script(
        # Gets all events for a trace code.
        description="Obtém todos os eventos de um código de rastreio.",
        gestures=["kb:nvda+control+e"]
    )
    def script_Gets_The_All_Event(self, gesture):
        request = RequestCorreios.RequestCorreios()
        clipboardCode = api.getClipData()
        try:
            tracking = request.get_tracking(clipboardCode)

            if tracking['quantidade'] == 0:
                # If events are not returned in the api.
                ui.message(
                    "Não foi possível obter os dados do código informado. Se a remeça foi enviada recentimente, aguarde até 24 horas e tente novamente!")
                return

            # loop through the events, and add them all to a string.
            for event in tracking['eventos']:
                Date_And_Time = f"{event['data']} {event['hora']}"
                substatus_text = ", ".join(event['subStatus'])
                events += f"{event['status']}, em {event['local']}, {substatus_text}. Data: {Date_And_Time}\n"

                ui.browseableMessage(events, title=clipboardCode)
        except Exception as e:
            ui.message(str(e))

    @script(
        # Gets events for a user-entered trace code.
        description="Obtém eventos para um código de rastreio digitado pelo usuário.",
        gestures=["kb:nvda+shift+control+e"]
    )
    def script_Gets_Events_By_User_Code(self, gesture):
        dlg = wx.TextEntryDialog(
            gui.mainFrame, "Digite o código de rastreio.", "código de rastreio")
        code = ""

        def callback(result):
            if result == wx.ID_OK:
                code = dlg.GetValue()
                request = RequestCorreios.RequestCorreios()
                try:
                    tracking = request.get_tracking(code)

                    if tracking['quantidade'] == 0:
                        # If events are not returned in the api.
                        ui.message(
                            "Não foi possível obter os dados do código informado. Se a remeça foi enviada recentimente, aguarde até 24 horas e tente novamente!")
                        return

                    events = f"Código: {code}\n"

            # loop through the events, and add them all to a string.
                    for event in tracking['eventos']:
                        Date_And_Time = f"{event['data']} {event['hora']}"
                        substatus_text = ", ".join(event['subStatus'])
                        events += f"{event['status']}, em {event['local']}, {substatus_text}. Data: {Date_And_Time}\n"

                    ui.browseableMessage(events, title="Eventos rastreio")
                except Exception as e:
                    ui.message(str(e))

        gui.runScriptModalDialog(dlg, callback)
