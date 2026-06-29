import wx

from modules.config import COLOR_FONDO, COLOR_SECUNDARIO
from modules.informe_pdf import armar_informe, generar_pdf


class InformePanel(wx.Panel):
    def __init__(self, parent, obtener_datos, obtener_agenda):
        super().__init__(parent)

        self.obtener_datos = obtener_datos
        self.obtener_agenda = obtener_agenda

        self.SetBackgroundColour(COLOR_FONDO)

        caja = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self, label="Vista previa del informe")
        titulo.SetForegroundColour("#7B5EA7")
        titulo.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        caja.Add(titulo, 0, wx.ALL | wx.CENTER, 10)

        boton_preview = wx.Button(self, label="Actualizar vista previa")
        boton_preview.Bind(wx.EVT_BUTTON, self.actualizar_preview)

        caja.Add(boton_preview, 0, wx.ALL | wx.EXPAND, 10)

        self.preview = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        caja.Add(self.preview, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 10)

        self.nombre_pdf = wx.TextCtrl(self, value="informe_nido.pdf")

        caja.Add(wx.StaticText(self, label="Nombre del PDF:"), 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        caja.Add(self.nombre_pdf, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 10)

        boton_pdf = wx.Button(self, label="Generar PDF")
        boton_pdf.SetBackgroundColour(COLOR_SECUNDARIO)
        boton_pdf.SetForegroundColour("white")
        boton_pdf.Bind(wx.EVT_BUTTON, self.crear_pdf)

        caja.Add(boton_pdf, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(caja)

    def obtener_texto_informe(self):
        datos = self.obtener_datos()
        agenda = self.obtener_agenda()
        return armar_informe(datos, agenda)

    def actualizar_preview(self, event):
        self.preview.SetValue(self.obtener_texto_informe())

    def crear_pdf(self, event):
        archivo = self.nombre_pdf.GetValue().strip()
        texto = self.obtener_texto_informe()

        archivo_generado = generar_pdf(archivo, texto)

        wx.MessageBox("PDF generado correctamente:\n" + archivo_generado, "NIDO")
