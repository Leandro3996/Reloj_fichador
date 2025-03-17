from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, date, timedelta, time
from ..models import (
    Operario, Area, Horario, Licencia, RegistroDiario,
    Horas_trabajadas, Horas_extras, Horas_feriado, Horas_totales,
    RegistroAsistencia, validate_file_extension
)
import os
from unittest.mock import patch, MagicMock
from django.conf import settings

class OperarioModelTest(TestCase):
    """Pruebas exhaustivas para el modelo Operario"""

    @classmethod
    def setUpTestData(cls):
        # Configuración inicial que se ejecuta una vez para todas las pruebas
        cls.area1 = Area.objects.create(nombre="Producción")
        cls.area2 = Area.objects.create(nombre="Mantenimiento")
        
        cls.horario1 = Horario.objects.create(
            nombre="Turno Mañana",
            hora_inicio=time(8, 0),
            hora_fin=time(16, 0)
        )
        
        cls.area1.horarios.add(cls.horario1)
        
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre="Juan",
            seg_nombre="Carlos",
            apellido="Pérez",
            seg_apellido="García",
            fecha_nacimiento=date(1985, 5, 15),
            fecha_ingreso_empresa=date(2010, 8, 1),
            titulo_tecnico=True,
            activo=True,
            descripcion="Operario con experiencia en maquinaria pesada."
        )
        cls.operario.areas.add(cls.area1)

    def test_campos_obligatorios(self):
        """Verifica que se apliquen las restricciones de campos obligatorios"""
        # Intentar crear un operario sin DNI (campo obligatorio)
        operario_invalido = Operario(
            nombre="María",
            apellido="González"
        )
        
        with self.assertRaises(IntegrityError):
            operario_invalido.save()
    
    def test_dni_unico(self):
        """Verifica que el DNI sea único"""
        # Intentar crear otro operario con el mismo DNI
        operario_duplicado = Operario(
            dni=12345678,  # Mismo DNI que el operario existente
            nombre="Pedro",
            apellido="López"
        )
        
        with self.assertRaises(IntegrityError):
            operario_duplicado.save()
    
    def test_campos_max_length(self):
        """Verifica la longitud máxima de varios campos"""
        campos = [
            ('nombre', 20),
            ('seg_nombre', 20),
            ('apellido', 20),
            ('seg_apellido', 20)
        ]
        
        for campo, longitud in campos:
            max_length = self.operario._meta.get_field(campo).max_length
            self.assertEqual(max_length, longitud, f"Campo {campo} no tiene longitud máxima esperada")
    
    def test_object_name_is_full_name_and_dni(self):
        """Verifica que el método __str__ del modelo devuelve el formato correcto"""
        expected_object_name = f"{self.operario.apellido} {self.operario.seg_apellido}, {self.operario.nombre} {self.operario.seg_nombre} - {self.operario.dni}"
        self.assertEqual(str(self.operario), expected_object_name)
        
        # Probar sin segundo nombre y apellido
        operario2 = Operario.objects.create(
            dni=87654321,
            nombre="María",
            apellido="González",
            activo=True
        )
        expected_name2 = f"González, María - 87654321"
        self.assertEqual(str(operario2), expected_name2)
    
    def test_operario_area_relationship(self):
        """Verifica que el operario está asociado al área correcta"""
        self.assertIn(self.area1, self.operario.areas.all())
        
        # Asignar una segunda área
        self.operario.areas.add(self.area2)
        self.assertEqual(self.operario.areas.count(), 2)
        
        # Verificar que se puede acceder a los horarios a través de las áreas
        for area in self.operario.areas.all():
            if area == self.area1:
                self.assertEqual(area.horarios.first(), self.horario1)
    
    def test_fecha_nacimiento_optional(self):
        """Verifica que la fecha de nacimiento es opcional"""
        operario_sin_fecha = Operario.objects.create(
            dni=98765432,
            nombre="Luis",
            apellido="Ramírez",
            activo=True
        )
        self.assertIsNone(operario_sin_fecha.fecha_nacimiento)
        self.assertTrue(operario_sin_fecha.activo)
    
    def test_historial_changes(self):
        """Verifica que se registran los cambios en el historial"""
        # Verificar que existe una entrada inicial en el historial
        self.assertEqual(self.operario.history.count(), 1)
        
        # Realizar un cambio
        self.operario.activo = False
        self.operario.save()
        
        # Verificar que se registró una nueva entrada en el historial
        self.assertEqual(self.operario.history.count(), 2)
        
        # Verificar que el cambio se registró correctamente
        ultimo_cambio = self.operario.history.first()
        self.assertEqual(ultimo_cambio.activo, False)
        
    def test_indexes(self):
        """Verifica que existen los índices definidos"""
        # Verificar que el modelo tiene los índices definidos
        indexes = [index.fields for index in Operario._meta.indexes]
        self.assertIn(['apellido'], indexes)
        self.assertIn(['dni'], indexes)


class AreaModelTest(TestCase):
    """Pruebas para el modelo Area"""
    
    @classmethod
    def setUpTestData(cls):
        cls.horario1 = Horario.objects.create(
            nombre="Turno Mañana",
            hora_inicio=time(8, 0),
            hora_fin=time(16, 0)
        )
        
        cls.horario2 = Horario.objects.create(
            nombre="Turno Tarde",
            hora_inicio=time(16, 0),
            hora_fin=time(0, 0)
        )
        
        cls.area = Area.objects.create(nombre="Producción")
        cls.area.horarios.add(cls.horario1, cls.horario2)
    
    def test_area_creation(self):
        """Verifica la creación básica de un área"""
        self.assertEqual(self.area.nombre, "Producción")
        self.assertEqual(str(self.area), "Producción")
    
    def test_area_horarios_relationship(self):
        """Verifica la relación entre áreas y horarios"""
        self.assertEqual(self.area.horarios.count(), 2)
        horarios = list(self.area.horarios.all())
        self.assertIn(self.horario1, horarios)
        self.assertIn(self.horario2, horarios)
        
        # Verificar eliminación de horario
        self.horario1.delete()
        self.assertEqual(self.area.horarios.count(), 1)
        self.assertEqual(self.area.horarios.first(), self.horario2)


class HorarioModelTest(TestCase):
    """Pruebas para el modelo Horario"""
    
    def test_horario_creation(self):
        """Verifica la creación básica de un horario"""
        horario = Horario.objects.create(
            nombre="Turno Nocturno",
            hora_inicio=time(22, 0),
            hora_fin=time(6, 0)
        )
        
        self.assertEqual(horario.nombre, "Turno Nocturno")
        self.assertEqual(horario.hora_inicio, time(22, 0))
        self.assertEqual(horario.hora_fin, time(6, 0))
    
    def test_horario_string_representation(self):
        """Verifica la representación en cadena del horario"""
        horario = Horario.objects.create(
            nombre="Turno Nocturno",
            hora_inicio=time(22, 0),
            hora_fin=time(6, 0)
        )
        
        expected_str = "Turno Nocturno: 22:00 - 06:00"
        self.assertEqual(str(horario), expected_str)


class LicenciaModelTest(TestCase):
    """Pruebas para el modelo Licencia"""
    
    @classmethod
    def setUpTestData(cls):
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre="Juan",
            apellido="Pérez",
            activo=True
        )
        
        # Crear un archivo PDF simulado para las pruebas
        cls.archivo_pdf = SimpleUploadedFile(
            "documento.pdf",
            b"contenido del archivo PDF",
            content_type="application/pdf"
        )
        
        cls.licencia = Licencia.objects.create(
            operario=cls.operario,
            archivo=cls.archivo_pdf,
            descripcion="Licencia médica por 15 días",
            fecha_inicio=date(2023, 1, 1),
            fecha_fin=date(2023, 1, 15)
        )
    
    def test_licencia_creation(self):
        """Verifica la creación básica de una licencia"""
        self.assertEqual(self.licencia.operario, self.operario)
        self.assertEqual(self.licencia.descripcion, "Licencia médica por 15 días")
        self.assertEqual(self.licencia.fecha_inicio, date(2023, 1, 1))
        self.assertEqual(self.licencia.fecha_fin, date(2023, 1, 15))
    
    def test_duracion_property(self):
        """Verifica el cálculo de la duración de la licencia"""
        self.assertEqual(self.licencia.duracion, 14)  # 15 - 1 = 14 días
        
        # Probar con licencia sin fechas
        licencia_sin_fechas = Licencia.objects.create(
            operario=self.operario,
            archivo=self.archivo_pdf,
            descripcion="Licencia sin fechas definidas"
        )
        self.assertIsNone(licencia_sin_fechas.duracion)
    
    def test_file_extension_validation(self):
        """Verifica la validación de extensiones de archivo"""
        # Archivo válido
        archivo_valido = SimpleUploadedFile(
            "documento.jpg",
            b"contenido del archivo JPG",
            content_type="image/jpeg"
        )
        
        # Debería ser válido
        validate_file_extension(archivo_valido)
        
        # Archivo inválido
        archivo_invalido = SimpleUploadedFile(
            "documento.txt",
            b"contenido del archivo TXT",
            content_type="text/plain"
        )
        
        # Debería lanzar ValidationError
        with self.assertRaises(ValidationError):
            validate_file_extension(archivo_invalido)


class RegistroAsistenciaModelTest(TestCase):
    """Pruebas para el modelo RegistroAsistencia"""
    
    @classmethod
    def setUpTestData(cls):
        # Crear un operario para las pruebas
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre='Prueba',
            apellido='Asistencia',
            activo=True
        )
        
        # Crear un registro de asistencia para hoy
        cls.fecha_hoy = timezone.now().date()
        cls.registro_asistencia = RegistroAsistencia.objects.create(
            operario=cls.operario,
            fecha=cls.fecha_hoy,
            estado_asistencia='ausente',
            estado_justificacion=False
        )

    def test_registro_asistencia_creation(self):
        """Verifica la creación básica de un registro de asistencia"""
        self.assertEqual(self.registro_asistencia.operario, self.operario)
        self.assertEqual(self.registro_asistencia.fecha, self.fecha_hoy)
        self.assertEqual(self.registro_asistencia.estado_asistencia, 'ausente')
        self.assertFalse(self.registro_asistencia.estado_justificacion)
    
    def test_verificar_asistencia_sin_registros(self):
        """Verifica que la asistencia sea ausente cuando no hay registros"""
        self.registro_asistencia.verificar_asistencia()
        self.assertEqual(self.registro_asistencia.estado_asistencia, 'ausente')
    
    def safe_datetime(self, year, month, day, hour, minute, second=0):
        """Crea un datetime que sea compatible con la configuración USE_TZ"""
        dt = datetime(year, month, day, hour, minute, second)
        if settings.USE_TZ:
            return timezone.make_aware(dt)
        return dt
    
    def test_verificar_asistencia_con_registros(self):
        """Verifica que la asistencia sea presente cuando hay registro de entrada"""
        # Crear un registro de entrada para hoy
        hora_entrada = self.safe_datetime(
            self.fecha_hoy.year, 
            self.fecha_hoy.month, 
            self.fecha_hoy.day, 
            8, 0
        )
        
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora_entrada,
            valido=True,
            inconsistencia=False
        )
        
        # Verificar asistencia
        self.registro_asistencia.verificar_asistencia()
        self.assertEqual(self.registro_asistencia.estado_asistencia, 'presente')
    
    def test_string_representation(self):
        """Verifica la representación en cadena del registro de asistencia"""
        expected_str = f"{self.operario} - {self.fecha_hoy} - ❌ Ausente"
        self.assertEqual(str(self.registro_asistencia), expected_str)
        
        # Cambiar a presente y verificar
        self.registro_asistencia.estado_asistencia = 'presente'
        self.registro_asistencia.save()
        expected_str = f"{self.operario} - {self.fecha_hoy} - ✅ Presente"
        self.assertEqual(str(self.registro_asistencia), expected_str)
    
    def test_unique_constraint(self):
        """Verifica la restricción de unicidad (operario, fecha)"""
        # Intentar crear otro registro para el mismo operario y fecha
        with self.assertRaises(IntegrityError):
            RegistroAsistencia.objects.create(
                operario=self.operario,
                fecha=self.fecha_hoy,
                estado_asistencia='presente'
            )


class HorasTotalesModelTest(TestCase):
    """Pruebas para el modelo Horas_totales"""
    
    @classmethod
    def setUpTestData(cls):
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre="Juan",
            apellido="Pérez",
            activo=True
        )
        
        cls.mes_actual = timezone.now().strftime('%Y-%m')
        
        cls.horas_totales = Horas_totales.objects.create(
            operario=cls.operario,
            mes_actual=cls.mes_actual,
            horas_normales=timedelta(hours=160),
            horas_nocturnas=timedelta(hours=20),
            horas_extras=timedelta(hours=15),
            horas_feriado=timedelta(hours=8)
        )
    
    def test_horas_totales_creation(self):
        """Verifica la creación básica de horas totales"""
        self.assertEqual(self.horas_totales.operario, self.operario)
        self.assertEqual(self.horas_totales.mes_actual, self.mes_actual)
        self.assertEqual(self.horas_totales.horas_normales, timedelta(hours=160))
        self.assertEqual(self.horas_totales.horas_nocturnas, timedelta(hours=20))
        self.assertEqual(self.horas_totales.horas_extras, timedelta(hours=15))
        self.assertEqual(self.horas_totales.horas_feriado, timedelta(hours=8))
    
    @patch('apps.reloj_fichador.models.Horas_trabajadas.objects.filter')
    @patch('apps.reloj_fichador.models.Horas_extras.objects.filter')
    @patch('apps.reloj_fichador.models.Horas_feriado.objects.filter')
    def test_calcular_horas_totales(self, mock_horas_feriado, mock_horas_extras, mock_horas_trabajadas):
        """Verifica el método de cálculo de horas totales"""
        # Configurar mocks para simular datos agregados
        mock_horas_trabajadas.return_value.aggregate.return_value = {
            'total_normales': timedelta(hours=160),
            'total_nocturnas': timedelta(hours=20)
        }
        
        mock_horas_extras.return_value.aggregate.return_value = {
            'total': timedelta(hours=15)
        }
        
        mock_horas_feriado.return_value.aggregate.return_value = {
            'total': timedelta(hours=8)
        }
        
        # Ejecutar el método
        resultado = Horas_totales.calcular_horas_totales(self.operario, self.mes_actual)
        
        # Verificar resultados
        self.assertEqual(resultado.horas_normales, timedelta(hours=160))
        self.assertEqual(resultado.horas_nocturnas, timedelta(hours=20))
        self.assertEqual(resultado.horas_extras, timedelta(hours=15))
        self.assertEqual(resultado.horas_feriado, timedelta(hours=8))


# Podemos agregar más clases de prueba para otros modelos si es necesario
