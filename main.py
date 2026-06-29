import wx
import os

from modules.config import COLOR_FONDO, COLOR_PRINCIPAL, COLOR_TEXTO, INTEGRANTES, UNIVERSIDAD, CARRERA
from modules.datos_panel import DatosPanel
from modules.agenda_panel import AgendaPanel
from modules.informe_panel import InformePanel


class NidoApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="NIDO - Agenda infantil", size=(900, 650))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(COLOR_FONDO)

        caja = wx.BoxSizer(wx.VERTICAL)

        caja.Add(self.crear_encabezado(panel), 0, wx.EXPAND)
        caja.Add(self.crear_perfil(panel), 0, wx.ALL | wx.EXPAND, 8)

        self.pestanas = wx.Notebook(panel)

        self.panel_datos = DatosPanel(self.pestanas, self.actualizar_perfil)
        self.panel_agenda = AgendaPanel(self.pestanas)
        self.panel_informe = InformePanel(
            self.pestanas,
            self.obtener_datos,
            self.obtener_agenda
        )

        self.pestanas.AddPage(self.panel_datos, "Datos")
        self.pestanas.AddPage(self.panel_agenda, "Agenda")
        self.pestanas.AddPage(self.panel_informe, "Informe")

        caja.Add(self.pestanas, 1, wx.ALL | wx.EXPAND, 8)

        caja.Add(self.crear_pie(panel), 0, wx.ALL | wx.CENTER, 8)

        panel.SetSizer(caja)

        self.Centre()
        self.Show()

    def crear_encabezado(self, parent):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(COLOR_PRINCIPAL)

        caja = wx.BoxSizer(wx.HORIZONTAL)

        if os.path.exists("logo_nido.png"):
            imagen = wx.Image("logo_nido.png", wx.BITMAP_TYPE_ANY)
            imagen = imagen.Scale(70, 70)
            logo = wx.StaticBitmap(panel, bitmap=wx.Bitmap(imagen))
        else:
            logo = wx.StaticText(panel, label="NIDO")

        titulo = wx.StaticText(panel, label="NIDO - Agenda")
        titulo.SetForegroundColour("white")
        titulo.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        caja.Add(logo, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        caja.Add(titulo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)

        panel.SetSizer(caja)
        return panel

    def crear_perfil(self, parent):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour("white")

        caja = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(panel, label="PERFIL")
        titulo.SetForegroundColour("#7B5EA7")
        titulo.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.perfil = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.perfil.SetValue("Todavia no se cargaron datos del niño.")
        self.perfil.SetMinSize((-1, 70))

        caja.Add(titulo, 0, wx.ALL, 5)
        caja.Add(self.perfil, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        panel.SetSizer(caja)
        return panel

    def crear_pie(self, parent):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(COLOR_FONDO)

        caja = wx.BoxSizer(wx.HORIZONTAL)

        if os.path.exists("logo_unpilar.png"):
            imagen = wx.Image("logo_unpilar.png", wx.BITMAP_TYPE_ANY)
            imagen = imagen.Scale(110, 40)
            logo_unpilar = wx.StaticBitmap(panel, bitmap=wx.Bitmap(imagen))
        else:
            logo_unpilar = wx.StaticText(panel, label="UNPILAR")

        texto = wx.StaticText(
            panel,
            label=INTEGRANTES + " - " + UNIVERSIDAD + " - Carrera: " + CARRERA
        )
        texto.SetForegroundColour(COLOR_TEXTO)

        caja.Add(logo_unpilar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        caja.Add(texto, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        panel.SetSizer(caja)
        return panel

    def actualizar_perfil(self, datos):
        self.perfil.SetValue(datos)

    def obtener_datos(self):
        return self.perfil.GetValue()

    def obtener_agenda(self):
        return self.panel_agenda.obtener_agenda()


app = wx.App()
ventana = NidoApp()
app.MainLoop()
