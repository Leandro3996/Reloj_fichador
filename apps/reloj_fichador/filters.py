from django import forms
from django.contrib.admin import DateFieldListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
import logging

class DateRangeWithYearFilter(DateRangeFilter):
    template = 'admin/date_range_with_year_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.year_field_name = f'{field_path}__year'
        self.params = params

    def choices(self, changelist):
        choices = super().choices(changelist)
        year_choices = [{'value': '', 'display': 'Select Year'}] + [
            {'value': year, 'display': year} for year in range(2000, 2031)
        ]
        for choice in choices:
            if 'value' in choice and choice['value'] == self.year_field_name:
                choice['year_choices'] = year_choices
        return choices

    def queryset(self, request, queryset):
        queryset = super().queryset(request, queryset)
        year = request.GET.get(self.year_field_name)
        if year:
            queryset = queryset.filter(**{self.year_field_name: year})
        return queryset


class ClientInfoFilter(logging.Filter):
    """
    Filtro para añadir información del cliente a los logs.
    Añade la dirección IP, el Host y el User-Agent a cada registro de log.
    """
    def filter(self, record):
        if not hasattr(record, 'ip'):
            record.ip = 'N/A'
        if not hasattr(record, 'host'):
            record.host = 'N/A'
        if not hasattr(record, 'agent'):
            record.agent = 'N/A'
            
        # Si hay información de solicitud en el contexto extra, extraerla
        if hasattr(record, 'request'):
            request = record.request
            record.ip = self._get_client_ip(request)
            record.host = request.META.get('HTTP_HOST', 'N/A')
            record.agent = request.META.get('HTTP_USER_AGENT', 'N/A')
            
        return True
    
    def _get_client_ip(self, request):
        """
        Obtiene la dirección IP real del cliente, incluso detrás de proxies.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Si hay varios IPs en X-Forwarded-For, tomar la primera (cliente original)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Si no hay X-Forwarded-For, usar la IP directa
            ip = request.META.get('REMOTE_ADDR', 'N/A')
        return ip

