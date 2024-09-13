# utils.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch  # Ya no será necesario usar "inch" directamente
from django.http import HttpResponse
from datetime import datetime
import os
from django.conf import settings
import openpyxl



# Helper para calcular el ancho de columnas basado en el contenido
def calcular_ancho_columnas(data, max_width):
    """
    Calcula el ancho de las columnas basado en el contenido.
    """
    # Encontrar el número máximo de columnas
    col_widths = [0] * len(data[0])

    # Calcular el ancho ideal para cada columna basado en el contenido
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell) * 6)  # Estimar ancho por caracteres (6 puntos por carácter)

    # Asegurar que el total de las columnas no exceda el ancho de la página
    total_width = sum(col_widths)
    scale_factor = max_width / total_width if total_width > max_width else 1
    col_widths = [w * scale_factor for w in col_widths]  # Ajustar a la página

    return col_widths


def generar_pdf(modeladmin, request, queryset, campos, encabezados, titulo,
                logo_path='img/logo_hores.png',
                logo_width_px=100, logo_height_px=50, logo_align='LEFT', logo_space_after=20,
                title_color='#EA8A2F', title_font_size=24, title_align='CENTER', title_space_after=20,
                title_font='Helvetica-Bold',
                header_bg_color='#F8C471', header_text_color='#000000',
                row_bg_color='#ffffff', row_text_color='#000000',
                table_border_color='#000000', table_border_width=1,
                cell_padding=12, col_widths=None,
                show_fecha_hora=True, fecha_hora_color='#000000', fecha_hora_font_size=10, fecha_hora_align='RIGHT',
                fecha_hora_space_after=10):

    # Respuesta HTTP para generar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{titulo}.pdf"'

    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # Obtener la ruta del logo desde la carpeta static
    logo_full_path = os.path.join(settings.STATIC_ROOT, logo_path)
    logo = Image(logo_full_path, width=logo_width_px, height=logo_height_px)

    # Crear el estilo para el título
    title = Paragraph(titulo, ParagraphStyle(
        name='title_style',
        fontName=title_font,
        fontSize=title_font_size,
        textColor=colors.HexColor(title_color),
        alignment=1 if title_align == 'CENTER' else (2 if title_align == 'RIGHT' else 0),
        spaceAfter=title_space_after
    ))

    # Fecha y hora actual
    if show_fecha_hora:
        fecha_hora = Paragraph(datetime.now().strftime('%d/%m/%Y %H:%M'), ParagraphStyle(
            name='fecha_hora_style',
            fontName='Helvetica',
            fontSize=fecha_hora_font_size,
            textColor=colors.HexColor(fecha_hora_color),
            alignment=1 if fecha_hora_align == 'CENTER' else (2 if fecha_hora_align == 'RIGHT' else 0),
            spaceAfter=fecha_hora_space_after
        ))
    else:
        fecha_hora = ''

    # Crear la tabla para el encabezado (logo, título, y fecha)
    header_data = [
        [logo, title, fecha_hora]
    ]
    header_table = Table(header_data, colWidths=[logo_width_px, None, 150])

    # Estilo de la tabla de encabezado
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Logo a la izquierda
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Título centrado
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Fecha a la derecha
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    # Añadir la tabla de encabezado
    elements.append(header_table)
    elements.append(Spacer(1, logo_space_after))

    # Preparar los datos para la tabla principal
    data = [encabezados]

    for obj in queryset:
        fila = []
        for campo in campos:
            valor = getattr(obj, campo)
            if callable(valor):
                valor = valor()
            fila.append(str(valor))
        data.append(fila)

    # Calcular el ancho de las columnas basado en el contenido y ajustado a la página A4
    if not col_widths:
        col_widths = calcular_ancho_columnas(data, A4[0] - 2 * inch)  # Restar márgenes de 1 pulgada a cada lado

    # Crear la tabla principal
    table = Table(data, colWidths=col_widths)

    # Estilo de la tabla principal
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_bg_color)),  # Color de fondo del encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(header_text_color)),  # Color del texto del encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), cell_padding),  # Padding inferior del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(row_bg_color)),  # Fondo de las filas de datos
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor(row_text_color)),  # Color del texto de las filas
        ('GRID', (0, 0), (-1, -1), table_border_width, colors.HexColor(table_border_color)),  # Bordes de la tabla
        ('BOX', (0, 0), (-1, -1), table_border_width, colors.HexColor(table_border_color)),  # Bordes externos
    ]))

    # Añadir la tabla principal
    elements.append(table)

    # Generar el PDF
    doc.build(elements)

    return response


def generar_excel(modeladmin, request, queryset, campos, encabezados, titulo):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = titulo

    sheet.append(encabezados)

    for obj in queryset:
        fila = []
        for campo in campos:
            valor = getattr(obj, campo)
            if callable(valor):
                valor = valor()
            fila.append(str(valor))
        sheet.append(fila)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{titulo}.xlsx"'
    workbook.save(response)
    return response
