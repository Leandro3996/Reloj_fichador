from django import forms
from .models import Licencia

class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['archivo', 'descripcion', 'fecha_inicio', 'fecha_fin']  # Incluye las fechas
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la licencia...'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'archivo': 'Cargar archivo de licencia (PDF, JPG, JPEG, PNG)',
            'descripcion': 'Descripción (opcional)',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin',
        }

    def __init__(self, *args, **kwargs):
        super(LicenciaForm, self).__init__(*args, **kwargs)
        self.fields['archivo'].required = False
