# utils.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch  # Ya no será necesario usar "inch" directamente
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import os
from django.conf import settings
import openpyxl
import threading
from contextlib import contextmanager
from io import BytesIO
from reportlab.pdfgen import canvas

_thread_locals = threading.local()

@contextmanager
def suppress_signal():
    _thread_locals.in_save = True
    try:
        yield
    finally:
        _thread_locals.in_save = False


# Helper para calcular el ancho de columnas basado en el contenido
def calcular_ancho_columnas(data, max_width):
    """
    Calcula el ancho de las columnas basado en el contenido.
    
    Args:
        data: Lista de listas con los datos de la tabla
        max_width: Ancho máximo disponible para la tabla
        
    Returns:
        Lista con los anchos calculados para cada columna
    """
    # Encontrar el número máximo de columnas
    num_cols = max(len(row) for row in data)
    col_widths = [0] * num_cols
    
    # Columnas que típicamente contienen nombres (para darles más espacio)
    columnas_nombres = {'nombre', 'apellido', 'nombr', 'apell', 'name', 'descripción', 'descripcion'}

    # Calcular el ancho ideal para cada columna basado en el contenido
    for row in data:
        for i, cell in enumerate(row):
            if i >= num_cols:  # Protección contra filas de longitud inconsistente
                continue
                
            # Estimar ancho basado en la longitud del contenido
            cell_str = str(cell)
            # Eliminar etiquetas HTML si existen
            if '<' in cell_str and '>' in cell_str:
                import re
                cell_str = re.sub(r'<[^>]+>', '', cell_str)
                
            cell_len = len(cell_str)
            # Ajustar el ancho basado en el tipo de contenido
            if cell_str.count('\n') > 0:  # Texto multilínea
                lines = cell_str.split('\n')
                cell_len = max(len(line) for line in lines)
            
            # Factor de anchura basado en tipo de columna
            width_factor = 7  # Puntos por carácter por defecto
            
            # Identificar si esta es una columna de nombres
            is_name_column = False
            if i < len(data[0]):  # Si es un encabezado
                header = str(data[0][i]).lower()
                # Si el encabezado contiene palabras relacionadas con nombres
                if any(kw in header for kw in columnas_nombres):
                    is_name_column = True
                    width_factor = 9  # Dar más espacio a columnas de nombres
            
            col_widths[i] = max(col_widths[i], cell_len * width_factor)

    # Asegurar anchos mínimos razonables basados en tipo de columna
    for i, width in enumerate(col_widths):
        if i < len(data[0]):
            header = str(data[0][i]).lower()
            if any(kw in header for kw in columnas_nombres):
                # Mínimo más alto para columnas de nombres
                col_widths[i] = max(width, 90)
            else:
                col_widths[i] = max(width, 50)

    # Asegurar que el total de las columnas no exceda el ancho de la página
    total_width = sum(col_widths)
    if total_width > max_width:
        # Reservar espacio mínimo para cada columna
        min_widths = [max(60, w * 0.6) for w in col_widths]
        min_total = sum(min_widths)
        
        # Distribuir el espacio restante proporcionalmente
        if min_total < max_width:
            remaining_width = max_width - min_total
            remaining_proportions = [max(0, w - min_w) for w, min_w in zip(col_widths, min_widths)]
            total_proportion = sum(remaining_proportions)
            
            if total_proportion > 0:
                for i in range(len(col_widths)):
                    extra = (remaining_proportions[i] / total_proportion) * remaining_width
                    col_widths[i] = min_widths[i] + extra
            else:
                # Si no hay proporciones restantes, mantener mínimos
                col_widths = min_widths
        else:
            # Si incluso los mínimos exceden el ancho, distribuir proporcionalmente
            ratio = max_width / min_total
            col_widths = [min_w * ratio for min_w in min_widths]
    
    return col_widths


def generar_pdf(modeladmin, request, queryset, campos, encabezados, titulo,
                logo_path='img/logo_hores.png',
                logo_width_px=120, logo_height_px=60, logo_align='LEFT', logo_space_after=15,
                # Nuevos colores corporativos más profesionales
                title_color='#2C3E50', title_font_size=20, title_align='LEFT', title_space_after=10,
                title_font='Helvetica-Bold',
                header_bg_color='#34495E', header_text_color='#FFFFFF',
                row_bg_color='#FFFFFF', row_text_color='#333333',
                accent_color='#3498DB',  # Color de acento para detalles
                table_border_color='#BDC3C7', table_border_width=0.5,
                cell_padding=8, col_widths=None,
                show_fecha_hora=True, fecha_hora_color='#7F8C8D', fecha_hora_font_size=9, fecha_hora_align='RIGHT',
                fecha_hora_space_after=5,
                calculate_hours_total=None):  # Nuevo parámetro para indicar si calcular totales de horas
    """
    Genera un reporte PDF con diseño profesional y empresarial
    
    Args:
        calculate_hours_total: Si es None, autodetecta. Si es True, fuerza el cálculo de totales.
                               Si es False, no calcula totales.
    """
    # Respuesta HTTP para generar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{titulo}.pdf"'

    # Crear el documento PDF
    doc = SimpleDocTemplate(
        response, 
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=40
    )
    elements = []
    
    # Definir nuevos estilos de texto
    styles = getSampleStyleSheet()
    custom_styles = {
        'title': ParagraphStyle(
            name='CustomTitle',
            fontName=title_font,
            fontSize=title_font_size,
            textColor=colors.HexColor(title_color),
            alignment=0,  # Izquierda
            spaceAfter=title_space_after,
            leading=title_font_size * 1.2
        ),
        'subtitle': ParagraphStyle(
            name='CustomSubtitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor(title_color),
            alignment=0,
            spaceAfter=8,
            leading=14
        ),
        'normal': ParagraphStyle(
            name='CustomNormal',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            alignment=0,
            leading=12
        ),
        'header_cell': ParagraphStyle(
            name='HeaderCell',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.HexColor(header_text_color),
            alignment=1,  # Centro
            leading=14
        ),
        'data_cell': ParagraphStyle(
            name='DataCell',
            fontName='Helvetica',
            fontSize=9.5,
            textColor=colors.HexColor(row_text_color),
            alignment=1,  # Centro
            leading=12,
            wordWrap='CJK'
        ),
        'name_cell': ParagraphStyle(
            name='NameCell',
            fontName='Helvetica',
            fontSize=9.5,
            textColor=colors.HexColor(row_text_color),
            alignment=1,  # Centro
            leading=12,
            wordWrap='CJK',
            splitLongWords=False
        ),
        'footer': ParagraphStyle(
            name='Footer',
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor(fecha_hora_color),
            alignment=1,  # Centro
            leading=10
        ),
        'total_label': ParagraphStyle(
            name='TotalLabel',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            alignment=2,  # Derecha
            leading=12
        ),
        'total_value': ParagraphStyle(
            name='TotalValue',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor(accent_color),
            alignment=1,  # Centro
            leading=12
        )
    }

    # Obtener la ruta del logo desde la carpeta static
    logo_full_path = os.path.join(settings.STATIC_ROOT, logo_path)
    logo = Image(logo_full_path, width=logo_width_px, height=logo_height_px)
    
    # Crear barra de color para el encabezado
    header_width = doc.width
    header_height = 5  # Altura de la barra de color
    header_bar = Table([['']], colWidths=[header_width], rowHeights=[header_height])
    header_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(accent_color)),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor(accent_color)),
    ]))

    # Crear tabla para encabezado con logo y título
    current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Título y subtítulo en un mismo contenedor
    title_container = []
    title_container.append(Paragraph(titulo, custom_styles['title']))
    
    # Subtítulo con información de filtros o detalles
    num_records = len(queryset)
    subtitle_text = f"{num_records} registro{'s' if num_records != 1 else ''}"
    title_container.append(Paragraph(subtitle_text, custom_styles['subtitle']))
    
    # Crear tabla de encabezado con el logo y título
    header_data = [
        [logo, title_container, Paragraph(current_date, ParagraphStyle(
            name='DateStyle',
            fontName='Helvetica',
            fontSize=fecha_hora_font_size,
            textColor=colors.HexColor(fecha_hora_color),
            alignment=2  # Derecha
        ))]
    ]
    
    header_table = Table(header_data, colWidths=[logo_width_px, doc.width - logo_width_px - 100, 100])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
    ]))

    # Añadir los elementos de encabezado
    elements.append(header_bar)
    elements.append(Spacer(1, 10))
    elements.append(header_table)
    elements.append(Spacer(1, 20))
    
    # Preparar línea separadora
    separator = Table([['']], colWidths=[doc.width], rowHeights=[1])
    separator.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor(table_border_color)),
    ]))
    
    elements.append(separator)
    elements.append(Spacer(1, 15))

    # Columnas que típicamente contienen nombres
    columnas_nombres = {'nombre', 'apellido', 'nombr', 'apell', 'name', 'descripción', 'descripcion'}
    
    # Detectar si este es un reporte con horas
    is_hours_report = calculate_hours_total is True
    hours_columns = []  # Índices de las columnas que contienen horas
    
    # Solo buscar columnas de horas si calculate_hours_total es True
    if is_hours_report:
        # Términos que indican columnas de horas
        terminos_horas = {'hora', 'horas', 'time', 'duracion', 'duración'}
        
        # 1. Detectar columnas por encabezado
        for i, header in enumerate(encabezados):
            header_lower = str(header).lower()
            if any(term in header_lower for term in terminos_horas):
                hours_columns.append(i)
        
        # 2. Si no hay coincidencias por encabezado, intentar por nombre de campo
        if not hours_columns:
            for i, campo in enumerate(campos):
                campo_lower = str(campo).lower()
                if any(term in campo_lower for term in terminos_horas):
                    hours_columns.append(i)
        
        # 3. Si aún no hay coincidencias, buscar por nombres específicos de columnas conocidas
        if not hours_columns:
            hora_campos = {'get_horas_normales', 'get_horas_nocturnas', 'get_horas_extras', 
                          'get_horas_feriado', 'horas_feriado', 'horas_extras'}
            for i, campo in enumerate(campos):
                if campo in hora_campos:
                    hours_columns.append(i)
        
        # Mensaje de depuración            
        print(f"DEBUG TOTALES: Reporte '{titulo}' - calculate_hours_total={calculate_hours_total}")
        print(f"DEBUG CAMPOS: {campos}")
        print(f"DEBUG ENCABEZADOS: {encabezados}")
        print(f"DEBUG COLUMNAS HORAS DETECTADAS: {hours_columns}")
                    
        # Si después de todo no hay columnas, desactivar el cálculo
        if not hours_columns:
            is_hours_report = False
                    
    # Diccionario para almacenar los totales de horas
    column_totals = {i: timedelta() for i in hours_columns}
    # Indicador de si tenemos valores de horas reales
    has_time_values = False

    # Preparar los datos para la tabla principal
    formatted_headers = []
    for header in encabezados:
        formatted_headers.append(Paragraph(header, custom_styles['header_cell']))
    
    data = [formatted_headers]
    raw_data = []  # Datos sin formato para calcular anchos

    for obj in queryset:
        fila = []
        raw_fila = []  # Para cálculo de anchos
        obj_values = []  # Valores originales para esta fila (para depuración)
        for i, campo in enumerate(campos):
            # Obtener valor (método del ModelAdmin, método del objeto o atributo)
            if hasattr(modeladmin, campo) and callable(getattr(modeladmin, campo)):
                metodo = getattr(modeladmin, campo)
                valor = metodo(obj)
            elif hasattr(obj, campo) and callable(getattr(obj, campo)):
                metodo = getattr(obj, campo)
                valor = metodo()
            else:
                try:
                    valor = getattr(obj, campo)
                except AttributeError:
                    valor = "—"  # Valor por defecto más estético
            
            # Guardar el valor original para cálculos
            valor_original = valor
            obj_values.append(valor_original)
            
            # Acumular totales si es una columna de horas y el valor es una duración
            if is_hours_report and i in hours_columns and isinstance(valor, timedelta):
                column_totals[i] += valor
                has_time_values = True  # Marcamos que tenemos al menos un valor de tiempo
                print(f"DEBUG VALOR HORAS: Col {i} ({campos[i]}): {valor}")
            
            # Formatear según tipo de dato
            if valor is None:
                valor = "—"  # Guión largo para campos vacíos (más estético)
            elif isinstance(valor, datetime):
                valor = valor.strftime('%d/%m/%Y %H:%M')
            elif isinstance(valor, date):
                valor = valor.strftime('%d/%m/%Y')
            elif isinstance(valor, timedelta):
                # Formato más legible para duraciones
                total_segundos = int(valor.total_seconds())
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                valor = f"{horas:02d}h {minutos:02d}m"
            
            # Limpiar HTML
            if hasattr(valor, '__html__') or (isinstance(valor, str) and ('<span' in valor.lower() or '<div' in valor.lower())):
                import re
                if '<span' in str(valor).lower():
                    if 'sí</span>' in str(valor).lower() or 'si</span>' in str(valor).lower():
                        valor = "Sí"
                    elif 'no</span>' in str(valor).lower():
                        valor = "No"
                    else:
                        valor = re.sub(r'<[^>]+>', '', str(valor))
                else:
                    valor = re.sub(r'<[^>]+>', '', str(valor))
            
            valor_str = str(valor)
            raw_fila.append(valor_str)
            
            # Determinar si esta columna contiene nombres
            is_name_column = False
            if i < len(encabezados):
                header = str(encabezados[i]).lower()
                if any(kw in header for kw in columnas_nombres):
                    is_name_column = True
            
            # Aplicar formato Paragraph con el estilo apropiado
            if is_name_column:
                valor_formateado = Paragraph(valor_str, custom_styles['name_cell'])
            else:
                valor_formateado = Paragraph(valor_str, custom_styles['data_cell'])
                
            fila.append(valor_formateado)
            
        data.append(fila)
        raw_data.append(raw_fila)

    # Calcular el ancho de las columnas
    if not col_widths:
        # Preparar datos para calcular anchos
        calc_data = [encabezados] + raw_data
        available_width = doc.width - 10
        col_widths = calcular_ancho_columnas(calc_data, available_width)

    # Crear la tabla principal con repetición de encabezados en cada página
    table = Table(data, colWidths=col_widths, repeatRows=1)

    # Estilo para la tabla principal
    table_style = [
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_bg_color)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(header_text_color)),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), cell_padding),
        ('TOPPADDING', (0, 0), (-1, 0), cell_padding),
        
        # Alineación
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Bordes más finos y elegantes
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor(table_border_color)),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor(table_border_color)),
        ('LINEAFTER', (0, 0), (-2, -1), 0.25, colors.HexColor(table_border_color)),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.HexColor(table_border_color)),
        
        # Resaltar línea bajo encabezados
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor(accent_color)),
        
        # Altura de fila
        ('ROWHEIGHT', (0, 0), (-1, -1), 28),
    ]
    
    # Colores alternados para filas (efecto cebra sutil)
    for i in range(1, len(data), 2):
        table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA')))
    
    table.setStyle(TableStyle(table_style))
    elements.append(table)

    # Agregar totales para reportes de horas
    if is_hours_report and hours_columns and has_time_values:
        print(f"DEBUG GENERANDO TOTALES: {has_time_values}")
        print(f"DEBUG TOTALES CALCULADOS: {column_totals}")
        
        elements.append(Spacer(1, 15))
        
        # Crear la tabla de totales
        total_headers = [''] * len(encabezados)
        total_values = [''] * len(encabezados)
        
        # Contador para verificar si tenemos totales que mostrar
        totales_a_mostrar = 0
        
        # Rellenar los totales
        for col_idx in hours_columns:
            if col_idx < len(encabezados):
                # Solo mostrar los totales para columnas que tienen valores
                if column_totals[col_idx].total_seconds() > 0:
                    totales_a_mostrar += 1
                    # Usar el encabezado original para el nombre del total
                    nombre_columna = encabezados[col_idx]
                    total_headers[col_idx] = Paragraph(f"Total {nombre_columna}:", custom_styles['total_label'])
                    
                    # Formatear el valor total de horas
                    total_td = column_totals[col_idx]
                    total_seconds = int(total_td.total_seconds())
                    total_hours = total_seconds // 3600
                    total_minutes = (total_seconds % 3600) // 60
                    
                    formatted_total = f"{total_hours:02d}h {total_minutes:02d}m"
                    total_values[col_idx] = Paragraph(formatted_total, custom_styles['total_value'])
        
        # Solo añadir la tabla de totales si hay al menos un total que mostrar
        if totales_a_mostrar > 0:
            totals_data = [total_headers, total_values]
            
            # Crear la tabla de totales
            totals_table = Table(totals_data, colWidths=col_widths)
            
            # Estilo para la tabla de totales
            totals_style = [
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor(accent_color)),
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F2F2F2')),
                ('ROWHEIGHT', (0, 0), (-1, -1), 25),
            ]
            
            totals_table.setStyle(TableStyle(totals_style))
            elements.append(totals_table)

    # Pie de página
    elements.append(Spacer(1, 30))
    footer_separator = Table([['']], colWidths=[doc.width], rowHeights=[1])
    footer_separator.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor(table_border_color)),
    ]))
    elements.append(footer_separator)
    elements.append(Spacer(1, 10))
    
    # Texto del pie de página con información relevante
    footer_text = f"Reporte generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • Total: {len(queryset)} registros"
    footer = Paragraph(footer_text, custom_styles['footer'])
    elements.append(footer)

    # Clase para agregar números de página
    class FooterCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            canvas.Canvas.__init__(self, *args, **kwargs)
            self.pages = []
            
        def showPage(self):
            self.pages.append(dict(self.__dict__))
            self._startPage()
            
        def save(self):
            page_count = len(self.pages)
            for page in self.pages:
                self.__dict__.update(page)
                self.draw_page_number(page_count)
                canvas.Canvas.showPage(self)
            canvas.Canvas.save(self)
            
        def draw_page_number(self, page_count):
            page_num = self._pageNumber
            text = f"Página {page_num} de {page_count}"
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor(fecha_hora_color))
            self.drawRightString(doc.width + 30, 20, text)
    
    # Generar el PDF con números de página
    buffer = BytesIO()
    doc.build(elements, canvasmaker=FooterCanvas)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
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


# ------------------------------------------------------------------------------------
# FUNCIONES PARA VALIDACIÓN DE DÍAS LABORALES Y GRUPOS DE SÁBADO
# ------------------------------------------------------------------------------------

def obtener_grupo_sabado_esperado(fecha_sabado):
    """
    Calcula el grupo que debe trabajar en un sábado específico siguiendo el patrón
    de alternancia global: 1er sábado del sistema = A, 2do = B, 3er = A, etc.

    Args:
        fecha_sabado: date (debe ser sábado)

    Returns:
        'A' o 'B'
    """
    from .models import RegistroDiario

    if fecha_sabado.weekday() != 5:  # No es sábado
        raise ValueError(f"{fecha_sabado} no es un sábado")

    # Obtener el primer sábado registrado en el sistema
    registro_mas_antiguo = RegistroDiario.objects.filter(
        valido=True,
        hora_fichada__isnull=False
    ).order_by('hora_fichada').first()

    if not registro_mas_antiguo:
        # Si no hay registros, asumir que es el primer sábado (grupo A)
        return 'A'

    fecha_inicio_sistema = registro_mas_antiguo.hora_fichada.date()

    # Mover a primer sábado del sistema
    dias_hasta_sabado = (5 - fecha_inicio_sistema.weekday()) % 7
    if dias_hasta_sabado == 0 and fecha_inicio_sistema.weekday() != 5:
        dias_hasta_sabado = 7
    primer_sabado_sistema = fecha_inicio_sistema + timedelta(days=dias_hasta_sabado)

    # Calcular número ordinal del sábado especificado
    semanas_desde_inicio = (fecha_sabado - primer_sabado_sistema).days // 7

    # Grupo A si es par, grupo B si es impar
    return 'A' if semanas_desde_inicio % 2 == 0 else 'B'


def es_dia_laboral(fecha, operario=None):
    """
    Determina si una fecha es día laboral considerando:
    1. CalendarioLaboral (feriados, paros, mantenimiento, etc.)
    2. Día de semana (domingos NUNCA son laborales)
    3. Sábados:
       - Primero verifica si el operario trabajó ese día (RegistroDiario - prioridad máxima)
       - Si trabajó, es laboral (intercambio o día asignado)
       - Si no hay registro pero está asignado a grupo, usa la lógica de alternancia
       - Si no está asignado, no es laboral
    4. Lunes a viernes (siempre laborales, salvo calendario)

    IMPORTANTE: Para sábados, siempre da prioridad a RegistroDiario (registros reales de trabajo)
    sobre GrupoSabado (asignaciones estándar). Esto permite capturar intercambios.

    Args:
        fecha: datetime.date o datetime.datetime
        operario: Operario object (opcional, requerido para validar sábados)

    Returns:
        bool: True si es día laboral, False en caso contrario
    """
    from datetime import date
    from django.utils import timezone

    # Convertir a date si es datetime
    if hasattr(fecha, 'date'):
        fecha = fecha.date()

    # 1. Verificar en CalendarioLaboral
    from .models import CalendarioLaboral
    try:
        calendario = CalendarioLaboral.objects.get(fecha=fecha)
        # Si existe un registro y NO es laborable, retornar False
        if calendario.es_no_laboral():
            return False
        # Si existe un registro y es laborable, continuar con otras validaciones
    except CalendarioLaboral.DoesNotExist:
        # Por defecto, si no existe registro en calendario, es laboral
        pass

    # 2. Domingos (weekday() == 6) NUNCA son laborales
    if fecha.weekday() == 6:
        return False

    # 3. Sábados (weekday() == 5) - validar con prioridad a registros reales
    if fecha.weekday() == 5:
        # Si no se proporciona operario, asumir que el sábado es laboral
        # (usado en la generación inicial de registros)
        if operario is None:
            return True

        # **PRIORIDAD 1: Verificar si operario trabajó ese sábado (RegistroDiario)**
        # Esto captura tanto asignaciones normales como intercambios
        if hay_intercambio_sabado(operario, fecha):
            return True

        # **PRIORIDAD 2: Verificar asignación de grupo (GrupoSabado)**
        # Buscar si operario está asignado a un grupo para esta fecha
        from .models import GrupoSabado
        grupo_activo = GrupoSabado.objects.filter(
            operario=operario,
            fecha_inicio__lte=fecha,
            fecha_fin__isnull=True,
        ).first() or GrupoSabado.objects.filter(
            operario=operario,
            fecha_inicio__lte=fecha,
            fecha_fin__gte=fecha,
        ).first()

        if not grupo_activo:
            # Operario no está asignado a grupo, no trabaja este sábado
            return False

        # Verificar lógica de alternancia de sábados
        # Cada sábado progresivo alterna: A, B, A, B, A, B...
        grupo_esperado = obtener_grupo_sabado_esperado(fecha)

        return grupo_activo.grupo == grupo_esperado

    # 4. Lunes a viernes (0-4) son siempre laborales (salvo calendario)
    return True


def obtener_sabados_operario(operario, mes, año):
    """
    Retorna lista de sábados que un operario debe trabajar en un mes y año determinados.

    Args:
        operario: Operario object
        mes: int (1-12)
        año: int (ej: 2025)

    Returns:
        list: Lista de dates (sábados a trabajar)
    """
    from datetime import date, timedelta
    from calendar import monthcalendar

    sabados_a_trabajar = []

    # Obtener todos los sábados del mes
    cal = monthcalendar(año, mes)
    sabados_del_mes = []

    for semana in cal:
        sabado_dia = semana[5]  # Sábado es índice 5 (lunes=0, domingo=6)
        if sabado_dia != 0:  # 0 significa que no está en este mes
            fecha_sabado = date(año, mes, sabado_dia)
            sabados_del_mes.append(fecha_sabado)

    # Verificar cuáles debe trabajar este operario
    for fecha_sabado in sabados_del_mes:
        if es_dia_laboral(fecha_sabado, operario):
            sabados_a_trabajar.append(fecha_sabado)

    return sabados_a_trabajar


def obtener_dias_laborales_mes(operario=None, mes=None, año=None):
    """
    Retorna lista de todas las fechas laborales de un mes.

    Args:
        operario: Operario object (opcional, afecta solo a sábados)
        mes: int (1-12), default = mes actual
        año: int, default = año actual

    Returns:
        list: Lista de dates (días laborales)
    """
    from datetime import date
    from calendar import monthrange
    from django.utils import timezone

    if mes is None:
        mes = timezone.now().month
    if año is None:
        año = timezone.now().year

    dias_laborales = []

    # Obtener último día del mes
    _, ultimo_dia = monthrange(año, mes)

    # Iterar cada día del mes
    for dia in range(1, ultimo_dia + 1):
        fecha = date(año, mes, dia)
        if es_dia_laboral(fecha, operario):
            dias_laborales.append(fecha)

    return dias_laborales


def obtener_feriados_mes(mes=None, año=None):
    """
    Retorna lista de todos los feriados/días no laborales de un mes.

    Args:
        mes: int (1-12), default = mes actual
        año: int, default = año actual

    Returns:
        list: Lista de tuplas (fecha, nombre, tipo_dia)
    """
    from datetime import date
    from calendar import monthrange
    from django.utils import timezone
    from .models import CalendarioLaboral

    if mes is None:
        mes = timezone.now().month
    if año is None:
        año = timezone.now().year

    # Obtener último día del mes
    _, ultimo_dia = monthrange(año, mes)

    # Obtener registros en calendario para este mes
    feriados = CalendarioLaboral.objects.filter(
        fecha__year=año,
        fecha__month=mes
    ).exclude(
        tipo_dia='laboral'
    ).order_by('fecha')

    return [(f.fecha, f.nombre, f.get_tipo_dia_display()) for f in feriados]


def horas_feriado_por_operario(operario, mes, año):
    """
    Calcula las horas de feriado que un operario dejó de trabajar en un mes.

    Args:
        operario: Operario object
        mes: int (1-12)
        año: int

    Returns:
        float: Horas de feriado (asumiendo 8 horas/día para lunes-viernes, 4 horas para sábado)
    """
    from .models import CalendarioLaboral
    from calendar import monthrange

    horas_total = 0
    _, ultimo_dia = monthrange(año, mes)

    # Verificar cada día del mes
    for dia in range(1, ultimo_dia + 1):
        from datetime import date
        fecha = date(año, mes, dia)

        # Verificar si es no-laboral en calendario
        try:
            cal = CalendarioLaboral.objects.get(fecha=fecha)
            if cal.es_no_laboral():
                # Contar como horas perdidas
                if fecha.weekday() == 5:  # Sábado
                    horas_total += 4  # Medio día
                else:  # Lunes-viernes
                    horas_total += 8  # Día completo
        except CalendarioLaboral.DoesNotExist:
            pass

    return horas_total


# ------------------------------------------------------------------------------------
# INTEGRACIÓN CON API DE FERIADOS ARGENTINA
# ------------------------------------------------------------------------------------

def calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin):
    """
    Calcula horas de enfermedad contando SOLO días laborales.

    Usa la función es_dia_laboral() para determinar si un día es laboral.
    Esto excluye:
    - Domingos (siempre no laborales)
    - Sábados (excepto si operario tiene grupo de sábado, pero aquí no aplica)
    - Feriados y días especiales del CalendarioLaboral

    Args:
        fecha_inicio (date): Primer día de licencia
        fecha_fin (date): Último día de licencia

    Returns:
        tuple: (dias_laborales_count, timedelta_horas_enfermedad)
               Retorna la cantidad de días contados y las horas totales

    Ejemplo:
        >>> from datetime import date
        >>> dias, horas = calcular_horas_enfermedad_laborales(
        ...     date(2025, 10, 27),  # Lunes
        ...     date(2025, 10, 31)   # Viernes
        ... )
        >>> print(dias, horas)
        5, timedelta(hours=40)
    """
    from datetime import timedelta

    dias_laborales = 0
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        # Usar la función es_dia_laboral() que ya tiene toda la lógica implementada
        # Sin pasar operario, solo verifica: calendario, domingos, y luego asume el resto como laboral
        if es_dia_laboral(fecha_actual, operario=None):
            dias_laborales += 1

        fecha_actual += timedelta(days=1)

    # Convertir días a horas (8 horas por día laboral)
    horas_enfermedad_total = timedelta(hours=dias_laborales * 8)

    return dias_laborales, horas_enfermedad_total


def obtener_feriados_api(año):
    """Consulta la API ArgentinaDatos y devuelve una lista normalizada de feriados."""
    import logging
    from datetime import date

    import requests

    logger = logging.getLogger('reloj_fichador')

    posibles_endpoints = [
        f"https://api.argentinadatos.com/v1/feriados/{año}",  # URL correcta según docs
        f"https://argentinadatos.com/api/v2/feriados/{año}",
        f"https://argentinadatos.com/api/v1/feriados/{año}",
        f"https://argentinadatos.com/v1/feriados/{año}",
        f"https://argentinadatos.com/feriados/{año}",
    ]

    for url in posibles_endpoints:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as exc:
            logger.warning(f"⚠️ No se pudo obtener feriados desde {url}: {exc}")
            continue
        except ValueError:
            logger.warning(f"⚠️ Respuesta inválida de la API de feriados ({url})")
            continue

        feriados = []

        def normalizar_tipo(tipo_raw):
            tipo_norm = (tipo_raw or '').lower()
            if tipo_norm in {'inamovible', 'nacional'}:
                return 'feriado_nacional'
            if tipo_norm in {'trasladable', 'móvil', 'movible', 'movil'}:
                return 'feriado_movible'
            return 'otro'

        registros = []
        if isinstance(data, dict):
            registros = data.get('feriados') or data.get('data') or []
        elif isinstance(data, list):
            registros = data

        for item in registros:
            if not isinstance(item, dict):
                continue

            fecha_str = item.get('fecha') or item.get('dia')
            if not fecha_str:
                continue

            try:
                fecha = date.fromisoformat(str(fecha_str))
            except ValueError:
                logger.warning(f"⚠️ Fecha de feriado inválida: {fecha_str}")
                continue

            nombre = item.get('motivo') or item.get('nombre') or 'Feriado sin nombre'
            tipo_sugerencia = normalizar_tipo(item.get('tipo'))

            feriados.append({
                'fecha': fecha,
                'nombre': nombre.strip(),
                'tipo_sugerencia': tipo_sugerencia,
                'datos_originales': item,
                'fuente_url': url,
            })

        if feriados:
            logger.info(f"✅ Se obtuvieron {len(feriados)} feriados de {url}")
            return feriados

    logger.error("❌ No se pudieron obtener feriados desde la API ArgentinaDatos")
    return []


# ------------------------------------------------------------------------------------
# DETECCIÓN DE GRUPOS DE SÁBADO
# ------------------------------------------------------------------------------------

def detectar_grupo_sabado_operario(operario, fecha_inicio_busqueda=None):
    """
    Detecta automáticamente el grupo (A o B) de un operario basándose en sus registros
    de trabajo en sábados del sistema RegistroDiario.

    Algoritmo:
    1. Busca todos los sábados donde el operario trabajó (tiene registros en RegistroDiario)
    2. Ordena estos sábados cronológicamente
    3. Asigna grupos alternando: 1er sábado = A, 2do = B, 3er = A, 4to = B, etc.
    4. El grupo del operario es el que corresponde al PRIMER sábado donde trabajó
    5. Si no hay registros de sábados, retorna None

    Args:
        operario: Instancia de Operario
        fecha_inicio_busqueda: (Opcional) Date para limitar búsqueda desde esta fecha

    Returns:
        Tupla (grupo, primer_sabado_trabajado) donde:
        - grupo: 'A', 'B' o None si no hay registros de sábados
        - primer_sabado_trabajado: Date del primer sábado donde trabajó, o None
    """
    from .models import RegistroDiario
    from django.db.models import Q

    # Buscar todos los registros del operario
    registros = RegistroDiario.objects.filter(
        operario=operario,
        valido=True,
        hora_fichada__isnull=False
    )

    if fecha_inicio_busqueda:
        registros = registros.filter(hora_fichada__date__gte=fecha_inicio_busqueda)

    # Extraer fechas únicas de sábados (weekday=5 en Python, 0=Monday)
    sabados_trabajados = set()
    for registro in registros:
        fecha = registro.hora_fichada.date()
        if fecha.weekday() == 5:  # Saturday
            sabados_trabajados.add(fecha)

    if not sabados_trabajados:
        return None, None

    # Ordenar sábados cronológicamente
    sabados_ordenados = sorted(sabados_trabajados)
    primer_sabado = sabados_ordenados[0]

    # Buscar el índice ordinal del primer sábado en la secuencia de todos los sábados
    # desde el inicio de los registros (o desde fecha_inicio_busqueda)
    fecha_inicio_sistema = fecha_inicio_busqueda
    if not fecha_inicio_sistema:
        # Obtener la fecha más antigua de cualquier registro en el sistema
        registro_mas_antiguo = RegistroDiario.objects.filter(
            valido=True,
            hora_fichada__isnull=False
        ).order_by('hora_fichada').first()

        if registro_mas_antiguo:
            fecha_inicio_sistema = registro_mas_antiguo.hora_fichada.date()
        else:
            # No hay registros en el sistema, asignar como primer sábado
            return 'A', primer_sabado

    # Calcular el número ordinal del primer sábado del operario
    # en la secuencia global de sábados del sistema
    fecha_actual = fecha_inicio_sistema
    # Mover a primer sábado del sistema
    dias_hasta_sabado = (5 - fecha_actual.weekday()) % 7
    if dias_hasta_sabado == 0 and fecha_actual.weekday() != 5:
        dias_hasta_sabado = 7
    fecha_actual = fecha_actual + timedelta(days=dias_hasta_sabado)

    indice_sabado = 0
    while fecha_actual < primer_sabado:
        indice_sabado += 1
        fecha_actual = fecha_actual + timedelta(weeks=1)

    # Asignar grupo: índice par = A, índice impar = B
    grupo = 'A' if indice_sabado % 2 == 0 else 'B'

    return grupo, primer_sabado


def obtener_grupo_sabado_operario(operario, fecha=None):
    """
    Obtiene el grupo de sábado para un operario en una fecha específica.

    Prioridad:
    1. Primero intenta obtener el grupo desde GrupoSabado (asignación manual)
    2. Si no existe asignación manual, detecta automáticamente desde RegistroDiario
    3. Si no hay registros históricos, retorna None

    Args:
        operario: Instancia de Operario
        fecha: (Opcional) Date para la cual obtener el grupo. Si es None, usa hoy.

    Returns:
        'A', 'B' o None
    """
    from .models import GrupoSabado
    from django.utils import timezone

    if fecha is None:
        fecha = timezone.now().date()

    # Buscar asignación manual activa
    grupo_sabado = GrupoSabado.objects.filter(
        operario=operario,
        fecha_inicio__lte=fecha
    ).exclude(
        fecha_fin__isnull=False,
        fecha_fin__lt=fecha
    ).order_by('-fecha_inicio').first()

    if grupo_sabado:
        return grupo_sabado.grupo

    # Si no hay asignación manual, detectar automáticamente
    grupo_auto, _ = detectar_grupo_sabado_operario(operario)
    return grupo_auto


def hay_intercambio_sabado(operario, fecha_sabado):
    """
    Verifica si hay un intercambio de sábado registrado en RegistroDiario.
    Un intercambio es cuando un operario trabaja un sábado que NO le corresponde
    a su grupo normal.

    Args:
        operario: Instancia de Operario
        fecha_sabado: Date del sábado a verificar

    Returns:
        True si hay registro de trabajo ese sábado, False en otro caso
    """
    from .models import RegistroDiario

    if fecha_sabado.weekday() != 5:  # No es sábado
        return False

    return RegistroDiario.objects.filter(
        operario=operario,
        hora_fichada__date=fecha_sabado,
        valido=True
    ).exists()
