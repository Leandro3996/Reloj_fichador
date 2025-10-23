"""
TEST DE DIAGNÓSTICO: Verifica si una licencia de 5 días crea registros para TODOS los días

Este test simula exactamente lo que describe el usuario:
- Luis se ausenta el lunes por licencia médica de 5 días
- El sistema debe marcar lunes, martes, miércoles, jueves y viernes como justificados
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
django.setup()

from django.test import TestCase
from django.utils import timezone
from datetime import date
from apps.reloj_fichador.models import (
    Operario, Licencia, RegistroAsistencia
)
from apps.reloj_fichador.tasks import procesar_licencia_aprobada


class TestLicencia5DiasCompletos(TestCase):
    """Diagnóstico: Licencia de 5 días debe crear 5 RegistroAsistencia justificados"""

    def setUp(self):
        """Crear operario de prueba"""
        self.operario = Operario.objects.create(
            nombre='Luis',
            apellido='García',
            dni=99999999,
            activo=True
        )

    def test_licencia_5_dias_completos(self):
        """
        CASO DE USO DEL USUARIO:
        Luis se ausenta el lunes por licencia médica de 5 días.
        Esperado: Marcar lunes, martes, miércoles, jueves y viernes como justificados
        """
        print("\n" + "="*100)
        print("TEST DE DIAGNÓSTICO: Licencia de 5 Días Completos")
        print("="*100)

        print("\n📋 ESCENARIO:")
        print("  - Operario: Luis García (DNI: 99999999)")
        print("  - Ausencia: Lunes a Viernes (5 días)")
        print("  - Licencia: Médica de 5 días")
        print("  - Esperado: 5 registros de asistencia justificados")

        # Crear licencia de lunes a viernes (5 días)
        fecha_inicio = date(2025, 10, 27)  # Lunes
        fecha_fin = date(2025, 10, 31)     # Viernes

        print(f"\n📅 FECHAS:")
        print(f"  Inicio: {fecha_inicio.strftime('%A, %d de %B de %Y')} (Lunes)")
        print(f"  Fin:    {fecha_fin.strftime('%A, %d de %B de %Y')} (Viernes)")

        licencia = Licencia.objects.create(
            operario=self.operario,
            descripcion='Licencia médica por enfermedad',
            fecha_subida=date.today(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='pendiente',
            aplicar_a_asistencia=True
        )

        print(f"\n✓ Licencia creada (Estado: PENDIENTE)")
        print(f"  ID: {licencia.pk}")
        print(f"  Duración: {(fecha_fin - fecha_inicio).days + 1} días")

        # PASO CRÍTICO: Aprobar la licencia
        print(f"\n🔄 Aprobando licencia...")
        licencia.estado = 'aprobada'
        licencia.save()
        print(f"✓ Licencia aprobada (Estado: APROBADA)")

        # PASO CRÍTICO: Ejecutar la tarea Celery
        print(f"\n⚙️  Ejecutando tarea Celery: procesar_licencia_aprobada()...")
        resultado = procesar_licencia_aprobada(licencia.pk)
        print(f"✓ Resultado: {resultado}")

        # VERIFICACIÓN: Contar registros creados
        print(f"\n🔍 VERIFICACIÓN:")
        registros = RegistroAsistencia.objects.filter(
            operario=self.operario,
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        ).order_by('fecha')

        print(f"  Total de registros encontrados: {registros.count()}")
        print(f"  Esperado: 5")

        if registros.count() != 5:
            print(f"\n❌ PROBLEMA DETECTADO: Solo se crearon {registros.count()} registros en lugar de 5")
        else:
            print(f"\n✅ CORRECTO: Se crearon todos los 5 registros")

        # Detallar cada día
        print(f"\n📊 DETALLE POR DÍA:")
        print(f"{'Fecha':<15} {'Día':<12} {'Estado':<15} {'Justificado':<12} {'Licencia':<10}")
        print("-" * 70)

        for i, registro in enumerate(registros, 1):
            dia_semana = registro.fecha.strftime('%A')
            estado = registro.get_estado_asistencia_display()
            justificado = "✓ Sí" if registro.estado_justificacion else "✗ No"
            licencia_id = registro.licencia_relacionada.pk if registro.licencia_relacionada else "N/A"

            print(f"{str(registro.fecha):<15} {dia_semana:<12} {estado:<15} {justificado:<12} {str(licencia_id):<10}")

            # Validar cada registro
            self.assertEqual(registro.estado_asistencia, RegistroAsistencia.ausente,
                           f"Día {i}: Estado debe ser 'ausente'")
            self.assertTrue(registro.estado_justificacion,
                          f"Día {i}: Debe estar justificado")
            self.assertEqual(registro.licencia_relacionada, licencia,
                           f"Día {i}: Debe vincularse a la licencia")

        # Resumen final
        print(f"\n{'='*70}")
        print("✅ TEST COMPLETADO: Todos los días están justificados correctamente")
        print("="*70 + "\n")

        # Aserciones finales
        self.assertEqual(registros.count(), 5, "Debe haber exactamente 5 registros")

        # Verificar que todos estén justificados
        justificados = registros.filter(estado_justificacion=True).count()
        self.assertEqual(justificados, 5, "Todos los 5 registros deben estar justificados")

        # Verificar que todos tengan la licencia vinculada
        con_licencia = registros.filter(licencia_relacionada=licencia).count()
        self.assertEqual(con_licencia, 5, "Todos deben tener la licencia vinculada")

        print("\n🎉 DIAGNOSTICO EXITOSO: El sistema funciona correctamente")


if __name__ == '__main__':
    import unittest
    unittest.main()
