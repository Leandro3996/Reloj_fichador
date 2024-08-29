# utils.py

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import openpyxl


def generar_pdf(modeladmin, request, queryset, campos, encabezados, titulo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{titulo}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph(titulo, styles['Title'])
    elements.append(title)

    data = [encabezados]

    for obj in queryset:
        fila = []
        for campo in campos:
            valor = getattr(obj, campo)
            if callable(valor):
                valor = valor()
            fila.append(str(valor))
        data.append(fila)

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

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
