"""
Test para validar la justificación retroactiva de ausencias.

Este test verifica el escenario real de negocio:
1. Empleado falta el día X (se crea RegistroAsistencia sin justificación)
2. Empleado presenta certificado el día Y (se carga la licencia)
3. Sistema retroactivamente justifica la ausencia del día X

Flujo:
├─ Crear RegistroAsistencia para días 1-5: ausente, SIN justificación
├─ Crear Licencia aprobada para esos mismos días
├─ Procesar la licencia
└─ Validar que todos los 5 días ahora están justificados y vinculados a la licencia
"""

import os
import django

# Configurar Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
django.setup()

from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from apps.reloj_fichador.models import (
    Operario, Licencia, RegistroAsistencia, HorasEnfermedad
)
from apps.reloj_fichador.tasks import procesar_licencia_aprobada


class TestJustificacionRetroactiva(TestCase):
    """Test suite para validar la justificación retroactiva de ausencias"""

    def setUp(self):
        """Crear datos de prueba"""
        self.operario = Operario.objects.create(
            nombre='Carlos',
            apellido='González',
            dni=87654321,
            activo=True
        )

    def test_escenario_real_ausencia_luego_licencia(self):
        """
        Escenario REAL de negocio:
        1. Empleado falta 5 días (28/10 al 1/11)
        2. Sistema crea 5 RegistroAsistencia: ausente, SIN justificación
        3. Empleado regresa el 1/11 con certificado médico
        4. Se carga licencia para 28/10 - 1/11 (aprobada)
        5. Sistema RETROACTIVAMENTE justifica los 5 días anteriores

        Validación:
        - Los 5 registros ahora tienen estado_justificacion=True
        - Los 5 registros están vinculados a la licencia
        - Se crea 1 HorasEnfermedad con 40 horas (5 días × 8)
        """
        print("\n" + "="*80)
        print("ESCENARIO REAL: Ausencia → Licencia (Retroactiva)")
        print("="*80)

        # PASO 1: Crear RegistroAsistencia PREVIOS sin justificación
        # (Como si el empleado hubiera faltado sin excusa)
        print("\n📋 PASO 1: Crear registros de ausencia SIN justificación")
        print("-" * 80)

        fecha_inicio_real = date(2025, 10, 28)  # Martes
        fecha_fin_real = date(2025, 11, 1)      # Sábado

        registros_sin_justificacion = []
        fecha_actual = fecha_inicio_real
        while fecha_actual <= fecha_fin_real:
            registro = RegistroAsistencia.objects.create(
                operario=self.operario,
                fecha=fecha_actual,
                estado_asistencia=RegistroAsistencia.ausente,
                estado_justificacion=False,  # ← SIN justificación
                descripcion=None
            )
            registros_sin_justificacion.append(registro)
            print(f"  ✓ Creado: {fecha_actual} - Ausente, NO justificado")
            fecha_actual += timedelta(days=1)

        print(f"\n  Total registros sin justificación: {len(registros_sin_justificacion)}")

        # Validar estado inicial
        registros_previos = RegistroAsistencia.objects.filter(
            operario=self.operario,
            fecha__gte=fecha_inicio_real,
            fecha__lte=fecha_fin_real
        )
        sin_justificacion_count = registros_previos.filter(estado_justificacion=False).count()
        print(f"  Estado inicial: {sin_justificacion_count}/5 sin justificación ✓")
        self.assertEqual(sin_justificacion_count, 5, "Deben haber 5 registros sin justificación")

        # PASO 2: Crear licencia APROBADA (posterior)
        # (Como si el empleado regresara el 1/11 con certificado)
        print("\n📋 PASO 2: Crear licencia aprobada (posterior a las ausencias)")
        print("-" * 80)

        licencia = Licencia.objects.create(
            operario=self.operario,
            descripcion='Licencia médica - Síndrome gripal',
            fecha_subida=date(2025, 11, 1),  # Se carga el día de reincorporación
            fecha_inicio=fecha_inicio_real,   # Pero cubre desde el 28/10
            fecha_fin=fecha_fin_real,
            estado='aprobada',  # ← APROBADA directamente
            aplicar_a_asistencia=True
        )

        print(f"  ✓ Licencia creada: {licencia}")
        print(f"    - Período: {fecha_inicio_real} a {fecha_fin_real}")
        print(f"    - Cargada: {date(2025, 11, 1)}")
        print(f"    - Duración esperada: 5 días = 40 horas")
        print(f"    - Estado: Aprobada")

        # PASO 3: Procesar licencia
        # (Esto debe disparar la lógica de justificación retroactiva)
        print("\n📋 PASO 3: Procesar licencia (ejecutar tarea Celery)")
        print("-" * 80)

        resultado = procesar_licencia_aprobada(licencia.pk)
        print(f"  ✓ Resultado: {resultado}")

        # PASO 4: VALIDACIÓN CRÍTICA
        print("\n" + "="*80)
        print("✅ VALIDACIÓN: Estado DESPUÉS de procesar licencia")
        print("="*80)

        # 4a. Validar RegistroAsistencia
        print("\n📋 RegistroAsistencia:")
        registros_actualizados = RegistroAsistencia.objects.filter(
            operario=self.operario,
            fecha__gte=fecha_inicio_real,
            fecha__lte=fecha_fin_real
        ).order_by('fecha')

        print(f"  Total registros: {registros_actualizados.count()}")

        justificados_count = 0
        for registro in registros_actualizados:
            estado = "✓ Justificado" if registro.estado_justificacion else "✗ SIN justificar"
            licencia_info = f"Licencia {registro.licencia_relacionada.pk}" if registro.licencia_relacionada else "N/A"
            print(f"    - {registro.fecha}: Ausente → {estado} | {licencia_info}")

            # VALIDAR: Debe estar justificado
            self.assertTrue(
                registro.estado_justificacion,
                f"Registro de {registro.fecha} debe estar justificado"
            )

            # VALIDAR: Debe estar vinculado a la licencia
            self.assertEqual(
                registro.licencia_relacionada,
                licencia,
                f"Registro de {registro.fecha} debe estar vinculado a la licencia"
            )

            justificados_count += 1

        print(f"\n  ✓ TOTAL JUSTIFICADOS: {justificados_count}/5")
        self.assertEqual(justificados_count, 5, "Los 5 registros deben estar justificados")

        # 4b. Validar HorasEnfermedad
        print("\n⏱️  HorasEnfermedad:")
        mes_periodo = fecha_inicio_real.strftime('%Y-%m')
        horas_enfermedad = HorasEnfermedad.objects.filter(
            operario=self.operario,
            licencia=licencia,
            mes_periodo=mes_periodo
        )

        self.assertEqual(horas_enfermedad.count(), 1, "Debe haber 1 registro de HorasEnfermedad")
        print(f"  ✓ Registros creados: 1")

        horas_obj = horas_enfermedad.first()
        horas_totales = int(horas_obj.horas_enfermedad.total_seconds() / 3600)

        print(f"  ✓ Horas acumuladas: {horas_totales}h (esperado: 40h)")
        self.assertEqual(horas_totales, 40, "Debe tener 40 horas (5 días × 8h)")

        print(f"  ✓ Mes período: {horas_obj.mes_periodo}")

        # 4c. Resumen final
        print("\n" + "="*80)
        print("🎯 RESULTADO FINAL")
        print("="*80)
        print(f"  ✓ Registros retroactivamente justificados: 5/5")
        print(f"  ✓ Horas de enfermedad acumuladas: 40h")
        print(f"  ✓ Licencia vinculada: {licencia.pk}")
        print(f"\n  ✅ ESCENARIO REAL VALIDADO CORRECTAMENTE")
        print("="*80 + "\n")

    def test_justificacion_retroactiva_dentro_30_dias(self):
        """
        Test: Validar que la justificación retroactiva respeta el límite de 30 días.

        Escenario:
        - Registros a diferentes distancias: -1, -5, -15, -29, -30 (DEBEN justificarse)
        - Registros a diferentes distancias: -31, -50 (NO DEBEN justificarse)
        - Licencia para hoy
        - Validar que respeta el límite de 30 días máximo
        """
        print("\n" + "="*80)
        print("TEST: Límite de 30 días para justificación retroactiva")
        print("="*80)

        fecha_licencia = date(2025, 11, 1)

        # Crear registros a diferentes distancias
        print("\n  Creando registros a diferentes distancias...")
        registros_info = [
            (1, True, "1 día antes - DEBE justificarse"),
            (5, True, "5 días antes - DEBE justificarse"),
            (15, True, "15 días antes - DEBE justificarse"),
            (29, True, "29 días antes - DEBE justificarse"),
            (30, True, "30 días antes - DEBE justificarse (límite)"),
            (31, False, "31 días antes - NO debe justificarse (fuera de límite)"),
            (50, False, "50 días antes - NO debe justificarse (fuera de límite)"),
        ]

        for dias_antes, debe_justificarse, descripcion in registros_info:
            RegistroAsistencia.objects.create(
                operario=self.operario,
                fecha=fecha_licencia - timedelta(days=dias_antes),
                estado_asistencia=RegistroAsistencia.ausente,
                estado_justificacion=False,
                descripcion=descripcion
            )
            print(f"    - {descripcion}")

        # Crear licencia aprobada
        licencia = Licencia.objects.create(
            operario=self.operario,
            descripcion='Licencia para test de límite',
            fecha_subida=fecha_licencia,
            fecha_inicio=fecha_licencia,
            fecha_fin=fecha_licencia,
            estado='aprobada',
            aplicar_a_asistencia=True
        )

        print(f"\n  Procesando licencia...")
        # Procesar
        procesar_licencia_aprobada(licencia.pk)

        # Validar
        justificados = RegistroAsistencia.objects.filter(
            operario=self.operario,
            estado_justificacion=True,
            licencia_relacionada=licencia
        ).count()

        sin_justificar = RegistroAsistencia.objects.filter(
            operario=self.operario,
            estado_justificacion=False,
            licencia_relacionada__isnull=True
        ).count()

        print(f"\n  Resultados:")
        print(f"    ✓ Registros justificados (dentro de 30 días): {justificados}")
        print(f"    ✓ Registros SIN justificar (fuera de límite): {sin_justificar}")

        # La lógica justifica registros donde: 0 < dias_diferencia <= 30
        # Esto incluye: 1, 5, 15, 29, 30 días = 5 registros dentro del límite
        # + 1 registro que es la licencia misma = 6 justificados
        # (El día 31 y 50 están fuera y no se justifican)
        self.assertGreaterEqual(justificados, 5, "Debe haber al menos 5 registros justificados (dentro de 30 días)")
        self.assertEqual(sin_justificar, 2, "Debe haber 2 registros sin justificar (fuera de 30 días: 31 y 50)")

        print("\n  ✅ Límite de 30 días validado correctamente")


if __name__ == '__main__':
    import unittest
    unittest.main()
