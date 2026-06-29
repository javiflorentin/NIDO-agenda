import wx
import wx.adv

from modules.config import COLOR_FONDO, COLOR_SECUNDARIO, COLOR_TEXTO


class DatosPanel(wx.Panel):
    def __init__(self, parent, actualizar_perfil):
        super().__init__(parent)

        self.actualizar_perfil = actualizar_perfil
        self.SetBackgroundColour(COLOR_FONDO)

        caja = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self, label="Datos del niño")
        titulo.SetForegroundColour("#7B5EA7")
        titulo.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        caja.Add(titulo, 0, wx.ALL | wx.CENTER, 10)

        grilla = wx.FlexGridSizer(rows=4, cols=4, hgap=10, vgap=8)

        self.nombre = wx.TextCtrl(self, size=(190, -1))
        self.edad = wx.TextCtrl(self, size=(80, -1))
        self.fecha_nacimiento = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)

        self.responsable = wx.TextCtrl(self, size=(190, -1))
        self.telefono = wx.TextCtrl(self, size=(150, -1))

        self.grupo = wx.ComboBox(
            self,
            choices=["Seleccionar", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            style=wx.CB_READONLY,
            size=(130, -1)
        )
        self.grupo.SetSelection(0)

        self.alergias = wx.TextCtrl(self, size=(190, -1))
        self.medicacion = wx.TextCtrl(self, size=(190, -1))

        self.agregar_a_grilla(grilla, "Nombre:", self.nombre)
        self.agregar_a_grilla(grilla, "Edad:", self.edad)
        self.agregar_a_grilla(grilla, "Nacimiento:", self.fecha_nacimiento)
        self.agregar_a_grilla(grilla, "Responsable:", self.responsable)
        self.agregar_a_grilla(grilla, "Telefono:", self.telefono)
        self.agregar_a_grilla(grilla, "Grupo:", self.grupo)
        self.agregar_a_grilla(grilla, "Alergias:", self.alergias)
        self.agregar_a_grilla(grilla, "Medicacion:", self.medicacion)

        caja.Add(grilla, 0, wx.ALL | wx.CENTER, 10)

        etiqueta_obs = wx.StaticText(self, label="Observaciones:")
        etiqueta_obs.SetForegroundColour(COLOR_TEXTO)

        self.observaciones = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        caja.Add(etiqueta_obs, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        caja.Add(self.observaciones, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 15)

        boton = wx.Button(self, label="Guardar datos")
        boton.SetBackgroundColour(COLOR_SECUNDARIO)
        boton.SetForegroundColour("white")
        boton.Bind(wx.EVT_BUTTON, self.guardar_datos)

        caja.Add(boton, 0, wx.ALL | wx.EXPAND, 15)

        self.SetSizer(caja)

    def agregar_a_grilla(self, grilla, texto, control):
        etiqueta = wx.StaticText(self, label=texto)
        grilla.Add(etiqueta, 0, wx.ALIGN_CENTER_VERTICAL)
        grilla.Add(control, 0)

    def obtener_fecha(self, control):
        fecha = control.GetValue()
        dia = fecha.GetDay()
        mes = fecha.GetMonth() + 1
        anio = fecha.GetYear()
        return str(dia) + "/" + str(mes) + "/" + str(anio)

    def obtener_datos(self):
        texto = ""

        texto += "Nombre: " + self.nombre.GetValue() + "    "
        texto += "Edad: " + self.edad.GetValue() + "    "
        texto += "Nacimiento: " + self.obtener_fecha(self.fecha_nacimiento) + "\n"

        texto += "Responsable: " + self.responsable.GetValue() + "    "
        texto += "Telefono: " + self.telefono.GetValue() + "\n"

        texto += "Grupo: " + self.grupo.GetValue() + "    "
        texto += "Alergias: " + self.alergias.GetValue() + "    "
        texto += "Medicacion: " + self.medicacion.GetValue() + "\n"

        texto += "Observaciones: " + self.observaciones.GetValue()

        return texto

    def guardar_datos(self, event):
        datos = self.obtener_datos()
        self.actualizar_perfil(datos)
        wx.MessageBox("Datos guardados.", "NIDO")
