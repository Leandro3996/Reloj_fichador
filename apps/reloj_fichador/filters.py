from django import forms
from django.contrib.admin import DateFieldListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

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

