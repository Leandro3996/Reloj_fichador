from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from .models import Licencia


class LicenciaForm(forms.ModelForm):
    """
    Formulario profesional para carga de licencias de ausencia.
    Utiliza Django Crispy Forms con el template pack unfold_crispy para integración con Django Unfold.
    """

    class Meta:
        model = Licencia
        fields = ['archivo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'archivo': forms.FileInput(attrs={
                'accept': '.pdf,.jpg,.jpeg,.png',
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ej: Licencia por enfermedad, permiso personal, etc.',
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
            }),
        }
        labels = {
            'archivo': 'Archivo de justificación',
            'descripcion': 'Descripción o motivo',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin',
        }
        help_texts = {
            'archivo': 'Formatos permitidos: PDF, JPG, JPEG, PNG (máx. 5 MB)',
            'descripcion': 'Proporciona detalles sobre la razón de la licencia',
            'fecha_inicio': 'Primer día de la licencia',
            'fecha_fin': 'Último día de la licencia',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar campos opcionales
        self.fields['archivo'].required = False
        self.fields['descripcion'].required = False

        # Configurar FormHelper para Crispy Forms con template pack unfold_crispy
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  # La etiqueta form está en la plantilla
        self.helper.form_class = 'form-horizontal'

        # Layout profesional con secciones
        self.helper.layout = Layout(
            # Sección: Documento
            Fieldset(
                '📄 Documento de justificación',
                'archivo',
            ),

            # Sección: Descripción
            Fieldset(
                '📝 Detalles de la licencia',
                'descripcion',
            ),

            # Sección: Fechas en dos columnas
            Fieldset(
                '📅 Período de la licencia',
                Row(
                    Column('fecha_inicio', css_class='col-md-6'),
                    Column('fecha_fin', css_class='col-md-6'),
                ),
            ),
        )

    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Validar que la fecha de fin sea posterior o igual a la de inicio
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError(
                    'La fecha de fin debe ser posterior o igual a la fecha de inicio.'
                )

        return cleaned_data
