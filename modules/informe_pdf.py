from modules.config import INTEGRANTES, UNIVERSIDAD, CARRERA


def armar_informe(datos, agenda):
    texto = ""

    texto += "INFORME NIDO\n"
    texto += "Agenda infantil temporal\n"
    texto += "====================================\n\n"

    texto += "DATOS DEL NIÑO\n"
    texto += datos
    texto += "\n\n"

    texto += "AGENDA\n"
    texto += agenda
    texto += "\n\n"

    texto += "====================================\n"
    texto += INTEGRANTES + "\n"
    texto += UNIVERSIDAD + " - " + CARRERA + "\n"

    return texto


def dividir_lineas(texto, largo_maximo):
    lineas_finales = []

    for linea in texto.split("\n"):
        while len(linea) > largo_maximo:
            lineas_finales.append(linea[:largo_maximo])
            linea = linea[largo_maximo:]
        lineas_finales.append(linea)

    return lineas_finales


def preparar_texto_pdf(texto):
    datos = texto.encode("cp1252", errors="replace")
    salida = b""

    for caracter in datos:
        if caracter == 40:
            salida += b"\\("
        elif caracter == 41:
            salida += b"\\)"
        elif caracter == 92:
            salida += b"\\\\"
        else:
            salida += bytes([caracter])

    return salida


def crear_contenido_pagina(lineas, titulo):
    contenido = b""

    contenido += b"0.72 0.60 0.85 rg\n"
    contenido += b"0 752 595 90 re f\n"

    contenido += b"1 1 1 rg\n"
    contenido += b"BT /F1 22 Tf 50 790 Td (INFORME NIDO) Tj ET\n"

    contenido += b"0 0 0 rg\n"

    y = 720

    if titulo:
        contenido += b"BT /F1 14 Tf 50 "
        contenido += str(y).encode("ascii")
        contenido += b" Td "
        contenido += b"("
        contenido += preparar_texto_pdf(titulo)
        contenido += b") Tj ET\n"
        y -= 28

    for linea in lineas:
        contenido += b"BT /F1 10 Tf 50 "
        contenido += str(y).encode("ascii")
        contenido += b" Td "
        contenido += b"("
        contenido += preparar_texto_pdf(linea)
        contenido += b") Tj ET\n"
        y -= 16

    return contenido


def generar_pdf(nombre_archivo, texto_informe):
    if nombre_archivo == "":
        nombre_archivo = "informe_nido.pdf"

    if not nombre_archivo.endswith(".pdf"):
        nombre_archivo += ".pdf"

    lineas = dividir_lineas(texto_informe, 85)

    paginas = []
    lineas_por_pagina = 38

    for inicio in range(0, len(lineas), lineas_por_pagina):
        paginas.append(lineas[inicio:inicio + lineas_por_pagina])

    objetos = []

    objetos.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append(b"<< /Type /Pages /Kids [] /Count 0 >>")
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    ids_paginas = []

    for pagina in paginas:
        contenido = crear_contenido_pagina(pagina, "Agenda infantil temporal")
        id_contenido = len(objetos) + 1
        objetos.append(
            b"<< /Length " + str(len(contenido)).encode("ascii") + b" >>\nstream\n" +
            contenido +
            b"endstream"
        )

        id_pagina = len(objetos) + 1
        pagina_objeto = (
            b"<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 3 0 R >> >> "
            b"/Contents " + str(id_contenido).encode("ascii") + b" 0 R >>"
        )
        objetos.append(pagina_objeto)
        ids_paginas.append(id_pagina)

    kids = b" ".join([str(x).encode("ascii") + b" 0 R" for x in ids_paginas])
    objetos[1] = b"<< /Type /Pages /Kids [" + kids + b"] /Count " + str(len(ids_paginas)).encode("ascii") + b" >>"

    salida = b"%PDF-1.4\n"
    posiciones = []

    for numero, objeto in enumerate(objetos, start=1):
        posiciones.append(len(salida))
        salida += str(numero).encode("ascii") + b" 0 obj\n"
        salida += objeto + b"\n"
        salida += b"endobj\n"

    inicio_xref = len(salida)

    salida += b"xref\n"
    salida += b"0 " + str(len(objetos) + 1).encode("ascii") + b"\n"
    salida += b"0000000000 65535 f \n"

    for posicion in posiciones:
        salida += f"{posicion:010d} 00000 n \n".encode("ascii")

    salida += b"trailer\n"
    salida += b"<< /Size " + str(len(objetos) + 1).encode("ascii") + b" /Root 1 0 R >>\n"
    salida += b"startxref\n"
    salida += str(inicio_xref).encode("ascii") + b"\n"
    salida += b"%%EOF"

    with open(nombre_archivo, "wb") as archivo:
        archivo.write(salida)

    return nombre_archivo
