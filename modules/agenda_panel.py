import wx
import wx.adv

from modules.config import COLOR_FONDO, COLOR_SECUNDARIO, COLOR_TEXTO


class AgendaPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.SetBackgroundColour(COLOR_FONDO)

        caja = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self, label="Agenda del niño")
        titulo.SetForegroundColour("#7B5EA7")
        titulo.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        caja.Add(titulo, 0, wx.ALL | wx.CENTER, 10)

        fila = wx.BoxSizer(wx.HORIZONTAL)

        self.fecha_agenda = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)

        self.tipo = wx.ComboBox(
            self,
            choices=["Turno medico", "Vacuna", "Actividad escolar", "Medicacion", "Pendiente", "Otro"],
            style=wx.CB_READONLY,
            size=(170, -1)
        )
        self.tipo.SetSelection(0)

        self.hora = wx.TextCtrl(self, size=(100, -1))

        fila.Add(wx.StaticText(self, label="Fecha:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        fila.Add(self.fecha_agenda, 0, wx.ALL, 5)

        fila.Add(wx.StaticText(self, label="Tipo:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        fila.Add(self.tipo, 0, wx.ALL, 5)

        fila.Add(wx.StaticText(self, label="Hora:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        fila.Add(self.hora, 0, wx.ALL, 5)

        caja.Add(fila, 0, wx.ALL | wx.CENTER, 5)

        self.detalle = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        caja.Add(wx.StaticText(self, label="Detalle:"), 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        caja.Add(self.detalle, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        boton = wx.Button(self, label="Agregar a la agenda")
        boton.SetBackgroundColour(COLOR_SECUNDARIO)
        boton.SetForegroundColour("white")
        boton.Bind(wx.EVT_BUTTON, self.agregar_agenda)

        caja.Add(boton, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        self.agenda = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.agenda.SetValue("AGENDA CARGADA\n")

        caja.Add(self.agenda, 2, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        ayuda = wx.StaticText(
            self,
            label="La agenda queda editable: si hay un error, se puede corregir escribiendo directamente en esta caja."
        )
        ayuda.SetForegroundColour(COLOR_TEXTO)

        caja.Add(ayuda, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        self.SetSizer(caja)

    def obtener_fecha(self, control):
        fecha = control.GetValue()
        dia = fecha.GetDay()
        mes = fecha.GetMonth() + 1
        anio = fecha.GetYear()
        return str(dia) + "/" + str(mes) + "/" + str(anio)

    def agregar_agenda(self, event):
        texto = ""

        texto += "\nFecha: " + self.obtener_fecha(self.fecha_agenda)
        texto += " | Tipo: " + self.tipo.GetValue()
        texto += " | Hora: " + self.hora.GetValue()
        texto += "\nDetalle: " + self.detalle.GetValue()
        texto += "\n--------------------------------------\n"

        self.agenda.AppendText(texto)

        self.detalle.SetValue("")
        self.hora.SetValue("")

    def obtener_agenda(self):
        return self.agenda.GetValue()
