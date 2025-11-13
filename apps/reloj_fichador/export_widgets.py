"""
Widgets personalizados para django-import-export

Estos widgets resuelven el problema de exportar IDs en lugar de valores legibles.
Permiten exportar datos en formato humano-legible (nombres, fechas, Sí/No, etc.)
en lugar de IDs, códigos o valores booleanos.

Uso:
    from apps.reloj_fichador.export_widgets import (
        NombreCompletoWidget, SiNoWidget, FechaHoraWidget, ChoiceDisplayWidget
    )

    class MiResource(resources.ModelResource):
        operario = fields.Field(
            column_name='Operario',
            attribute='operario',
            widget=NombreCompletoWidget(Operario)
        )
"""

from import_export import widgets
from datetime import datetime


class NombreCompletoWidget(widgets.ForeignKeyWidget):
    """
    Widget para ForeignKey que exporta/importa el nombre completo.

    Exportación: Muestra "Apellido, Nombre" en lugar del ID
    Importación: Busca por DNI, ID o nombre completo

    Ejemplo:
        operario = fields.Field(
            column_name='Operario',
            attribute='operario',
            widget=NombreCompletoWidget(Operario)
        )
    """

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: buscar operario por DNI, ID o nombre completo
        """
        if not value:
            return None

        # Intentar buscar por ID (comportamiento por defecto)
        if str(value).isdigit():
            try:
                return self.model.objects.get(pk=int(value))
            except self.model.DoesNotExist:
                # Intentar por DNI si tiene ese campo
                if hasattr(self.model, 'dni'):
                    try:
                        return self.model.objects.get(dni=value)
                    except self.model.DoesNotExist:
                        pass

        # Intentar buscar por nombre completo "Apellido, Nombre"
        if ',' in str(value):
            try:
                apellido, nombre = str(value).split(',', 1)
                return self.model.objects.get(
                    apellido__iexact=apellido.strip(),
                    nombre__iexact=nombre.strip()
                )
            except (self.model.DoesNotExist, ValueError):
                pass

        # Fallback al comportamiento por defecto
        return super().clean(value, row, *args, **kwargs)

    def render(self, value, obj=None):
        """
        Exportación: mostrar "Apellido, Nombre" en lugar de ID
        """
        if value is None:
            return ""

        # Si tiene campos nombre y apellido
        if hasattr(value, 'nombre') and hasattr(value, 'apellido'):
            return f"{value.apellido}, {value.nombre}"

        # Si solo tiene nombre
        if hasattr(value, 'nombre'):
            return value.nombre

        # Fallback al __str__ del modelo
        return str(value)


class ChoiceDisplayWidget(widgets.Widget):
    """
    Widget para campos con choices que exporta el "display name".

    Exportación: Muestra el texto legible en lugar del código
    Importación: Acepta tanto el código como el texto legible

    Ejemplo:
        tipo_movimiento = fields.Field(
            column_name='Tipo de Movimiento',
            attribute='tipo_movimiento',
            widget=ChoiceDisplayWidget(RegistroDiario.TIPO_CHOICES)
        )
    """

    def __init__(self, choices, *args, **kwargs):
        """
        Args:
            choices: Las choices del modelo (ej: Model.FIELD_CHOICES)
        """
        self.choices = dict(choices) if choices else {}
        self.reverse_choices = {v.lower(): k for k, v in self.choices.items()}
        super().__init__(*args, **kwargs)

    def render(self, value, obj=None):
        """
        Exportación: mostrar el display name

        Ejemplo: "entrada" → "Entrada"
        """
        if value is None or value == '':
            return ""
        return self.choices.get(value, str(value))

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: aceptar tanto el código como el display name

        Ejemplo: "Entrada" → "entrada"
        """
        if not value:
            return None

        # Si ya es el código correcto, retornarlo
        if value in self.choices:
            return value

        # Intentar buscar por display name (case insensitive)
        value_lower = str(value).lower().strip()
        if value_lower in self.reverse_choices:
            return self.reverse_choices[value_lower]

        # Si no se encuentra, retornar el valor original
        # (dejará que Django maneje el error de validación)
        return value


class SiNoWidget(widgets.BooleanWidget):
    """
    Widget para campos booleanos que exporta Sí/No en lugar de True/False.

    Exportación: Muestra "Sí" o "No"
    Importación: Acepta múltiples variaciones (Sí, Si, Yes, 1, True, etc.)

    Ejemplo:
        valido = fields.Field(
            column_name='Válido',
            attribute='valido',
            widget=SiNoWidget()
        )
    """

    def render(self, value, obj=None):
        """
        Exportación: mostrar Sí/No en lugar de True/False
        """
        if value is None:
            return ""
        return "Sí" if value else "No"

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: aceptar múltiples variaciones

        Acepta: Sí, Si, sí, si, Yes, yes, True, true, 1
        """
        if value is None or value == '':
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return bool(value)

        if isinstance(value, str):
            value_lower = value.lower().strip()
            return value_lower in ('sí', 'si', 'yes', 'true', '1', 'verdadero')

        return bool(value)


class FechaHoraWidget(widgets.DateTimeWidget):
    """
    Widget para fechas que exporta en formato español legible.

    Exportación: Formato "dd/mm/yyyy hh:mm:ss"
    Importación: Acepta múltiples formatos

    Ejemplo:
        hora_fichada = fields.Field(
            column_name='Fecha y Hora',
            attribute='hora_fichada',
            widget=FechaHoraWidget()
        )
    """

    def __init__(self, formato='%d/%m/%Y %H:%M:%S'):
        """
        Args:
            formato: Formato de fecha para exportación (default: dd/mm/yyyy hh:mm:ss)
        """
        super().__init__(format=formato)
        self.formato_export = formato

    def render(self, value, obj=None):
        """
        Exportación: formato español legible
        """
        if not value:
            return ""

        if isinstance(value, str):
            return value

        try:
            return value.strftime(self.formato_export)
        except (AttributeError, ValueError):
            return str(value)

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: acepta múltiples formatos de fecha
        """
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        # Formatos comunes a intentar
        formatos = [
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y %H:%M',
        ]

        for formato in formatos:
            try:
                return datetime.strptime(str(value), formato)
            except ValueError:
                continue

        # Fallback al comportamiento por defecto
        return super().clean(value, row, *args, **kwargs)


class FechaWidget(widgets.DateWidget):
    """
    Widget para fechas (sin hora) que exporta en formato español.

    Exportación: Formato "dd/mm/yyyy"
    Importación: Acepta múltiples formatos

    Ejemplo:
        fecha = fields.Field(
            column_name='Fecha',
            attribute='fecha',
            widget=FechaWidget()
        )
    """

    def __init__(self, formato='%d/%m/%Y'):
        super().__init__(format=formato)
        self.formato_export = formato

    def render(self, value, obj=None):
        """Exportación: formato dd/mm/yyyy"""
        if not value:
            return ""

        if isinstance(value, str):
            return value

        try:
            return value.strftime(self.formato_export)
        except (AttributeError, ValueError):
            return str(value)

    def clean(self, value, row=None, *args, **kwargs):
        """Importación: acepta múltiples formatos"""
        if not value:
            return None

        from datetime import date

        if isinstance(value, (date, datetime)):
            return value if isinstance(value, date) else value.date()

        # Formatos comunes
        formatos = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
        ]

        for formato in formatos:
            try:
                return datetime.strptime(str(value), formato).date()
            except ValueError:
                continue

        return super().clean(value, row, *args, **kwargs)


class TimeDeltaWidget(widgets.Widget):
    """
    Widget para campos timedelta que exporta en formato legible de horas.

    Exportación: Formato "XXh YYm" (ej: "08h 30m")
    Importación: Acepta formatos como "8:30", "8h 30m", "8.5"

    Ejemplo:
        horas_normales = fields.Field(
            column_name='Horas Normales',
            attribute='horas_normales',
            widget=TimeDeltaWidget()
        )
    """

    def render(self, value, obj=None):
        """
        Exportación: formato "XXh YYm"
        """
        if value is None:
            return ""

        if isinstance(value, str):
            return value

        from datetime import timedelta

        if isinstance(value, timedelta):
            total_segundos = int(value.total_seconds())
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            return f"{horas:02d}h {minutos:02d}m"

        return str(value)

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: acepta "8:30", "8h 30m", "8.5", etc.
        """
        if not value:
            return None

        from datetime import timedelta

        if isinstance(value, timedelta):
            return value

        value_str = str(value).strip()

        # Formato "8h 30m"
        if 'h' in value_str:
            try:
                parts = value_str.replace('m', '').split('h')
                horas = int(parts[0].strip())
                minutos = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 0
                return timedelta(hours=horas, minutes=minutos)
            except (ValueError, IndexError):
                pass

        # Formato "8:30"
        if ':' in value_str:
            try:
                parts = value_str.split(':')
                horas = int(parts[0])
                minutos = int(parts[1]) if len(parts) > 1 else 0
                return timedelta(hours=horas, minutes=minutos)
            except (ValueError, IndexError):
                pass

        # Formato decimal "8.5"
        try:
            horas_decimal = float(value_str)
            return timedelta(hours=horas_decimal)
        except ValueError:
            pass

        return None


class DecimalHorasWidget(widgets.Widget):
    """
    Widget para mostrar timedelta como decimal de horas.

    Exportación: Formato "8.50" (8 horas y 30 minutos = 8.5)

    Ejemplo:
        horas_totales = fields.Field(
            column_name='Total Horas',
            attribute='horas_totales',
            widget=DecimalHorasWidget()
        )
    """

    def render(self, value, obj=None):
        """
        Exportación: mostrar horas como decimal
        """
        if value is None:
            return ""

        from datetime import timedelta

        if isinstance(value, timedelta):
            total_horas = value.total_seconds() / 3600
            return f"{total_horas:.2f}"

        if isinstance(value, (int, float)):
            return f"{float(value):.2f}"

        return str(value)

    def clean(self, value, row=None, *args, **kwargs):
        """
        Importación: convertir decimal a timedelta
        """
        if not value:
            return None

        from datetime import timedelta

        try:
            horas = float(value)
            return timedelta(hours=horas)
        except (ValueError, TypeError):
            return None
