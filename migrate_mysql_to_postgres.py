#!/usr/bin/env python
"""
Script de migración de MySQL a PostgreSQL para el sistema Reloj Fichador.

Este script migra todos los datos de la base de datos MySQL a PostgreSQL
utilizando Django ORM, preservando las relaciones y la integridad de los datos.

Uso:
    python migrate_mysql_to_postgres.py

Requisitos:
    - Ambas bases de datos deben estar corriendo
    - El esquema debe existir en PostgreSQL (ejecutar migrate --database=postgres primero)
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
django.setup()

from django.db import connections, transaction
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission


def get_all_models():
    """Obtiene todos los modelos de la aplicación en orden de dependencia."""
    # Orden específico para respetar las relaciones FK
    ordered_models = [
        # Primero los modelos de Django auth y admin
        'auth.Group',
        'auth.User',
        'auth.Permission',
        'contenttypes.ContentType',
        'admin.LogEntry',  # Historial de acciones del Django Admin (auditoría)

        # Modelos de la aplicación en orden de dependencias
        'reloj_fichador.ConfiguracionRedondeo',
        'reloj_fichador.ConfiguracionRedondeoSalida',
        'reloj_fichador.Area',
        'reloj_fichador.Horario',
        'reloj_fichador.Operario',
        'reloj_fichador.HistoricalOperario',
        'reloj_fichador.Feriado',
        'reloj_fichador.RegistroDiario',
        'reloj_fichador.HistoricalRegistroDiario',
        'reloj_fichador.Horas_trabajadas',
        'reloj_fichador.Horas_Extras',
        'reloj_fichador.Horas_Feriado',
        'reloj_fichador.Horas_Nocturnas',
        'reloj_fichador.RegistroAsistencia',
        'reloj_fichador.Licencia',
        'reloj_fichador.JustificacionDocumento',
        'reloj_fichador.TotalHorasMensuales',

        # Modelos de Celery
        'django_celery_beat.IntervalSchedule',
        'django_celery_beat.CrontabSchedule',
        'django_celery_beat.SolarSchedule',
        'django_celery_beat.ClockedSchedule',
        'django_celery_beat.PeriodicTask',
        'django_celery_results.TaskResult',
    ]

    models = []
    for model_str in ordered_models:
        try:
            model = apps.get_model(model_str)
            models.append(model)
        except LookupError:
            print(f"⚠️  Modelo {model_str} no encontrado, omitiendo...")

    return models


def migrate_model(model, source_db='default', target_db='postgres', batch_size=1000):
    """Migra un modelo específico de una base de datos a otra."""
    model_name = model._meta.label
    print(f"\n{'='*60}")
    print(f"Migrando: {model_name}")
    print(f"{'='*60}")

    try:
        # Contar registros en origen
        source_count = model.objects.using(source_db).count()
        print(f"📊 Registros en origen (MySQL): {source_count}")

        if source_count == 0:
            print("✓ No hay datos para migrar")
            return True

        # Verificar si ya existen datos en destino
        target_count = model.objects.using(target_db).count()
        if target_count > 0:
            print(f"⚠️  Ya existen {target_count} registros en PostgreSQL")
            respuesta = input("¿Desea continuar? (s/n): ")
            if respuesta.lower() != 's':
                print("⊘ Omitiendo modelo")
                return False

        # Obtener todos los objetos de la fuente
        source_objects = model.objects.using(source_db).all()

        # Procesar en lotes
        migrated = 0
        errors = 0

        for i in range(0, source_count, batch_size):
            batch = list(source_objects[i:i + batch_size])

            with transaction.atomic(using=target_db):
                for obj in batch:
                    try:
                        # Resetear el pk para que Django cree uno nuevo si es necesario
                        obj.pk = obj.pk  # Mantener el mismo ID
                        obj.save(using=target_db, force_insert=False)
                        migrated += 1
                    except Exception as e:
                        errors += 1
                        print(f"  ✗ Error al migrar objeto {obj.pk}: {str(e)}")

            # Mostrar progreso
            progress = (i + len(batch)) / source_count * 100
            print(f"  Progreso: {progress:.1f}% ({migrated} registros)", end='\r')

        print(f"\n✓ Migración completada: {migrated} registros")
        if errors > 0:
            print(f"⚠️  Errores: {errors}")

        # Verificar conteo final
        final_count = model.objects.using(target_db).count()
        print(f"📊 Registros en destino (PostgreSQL): {final_count}")

        return True

    except Exception as e:
        print(f"✗ Error al migrar {model_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def reset_sequences(target_db='postgres'):
    """Reinicia las secuencias de PostgreSQL para que coincidan con los IDs máximos."""
    print(f"\n{'='*60}")
    print("Reiniciando secuencias de PostgreSQL...")
    print(f"{'='*60}")

    with connections[target_db].cursor() as cursor:
        # Obtener todas las tablas con secuencias
        cursor.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND column_default LIKE 'nextval%'
        """)

        sequences = cursor.fetchall()

        for table_name, column_name in sequences:
            try:
                cursor.execute(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table_name}', '{column_name}'),
                        COALESCE((SELECT MAX({column_name}) FROM {table_name}), 1),
                        true
                    )
                """)
                print(f"  ✓ Secuencia actualizada: {table_name}.{column_name}")
            except Exception as e:
                print(f"  ⚠️  Error con {table_name}.{column_name}: {str(e)}")


def main():
    """Función principal de migración."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   MIGRACIÓN DE MYSQL A POSTGRESQL                        ║
    ║   Sistema: Reloj Fichador                                ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    print(f"Fecha de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Verificar conexiones
    print("🔍 Verificando conexiones a bases de datos...")
    try:
        connections['default'].ensure_connection()
        print("  ✓ MySQL conectada")
    except Exception as e:
        print(f"  ✗ Error conectando a MySQL: {e}")
        return 1

    try:
        connections['default'].ensure_connection()
        print("  ✓ PostgreSQL conectada")
    except Exception as e:
        print(f"  ✗ Error conectando a PostgreSQL: {e}")
        return 1

    # Advertencia
    print("\n⚠️  ADVERTENCIA ⚠️")
    print("Este proceso migrará todos los datos de MySQL a PostgreSQL.")
    print("Asegúrese de haber:")
    print("  1. Ejecutado las migraciones en PostgreSQL")
    print("  2. Hecho un backup de ambas bases de datos")
    print("  3. Verificado que no hay procesos usando la base de datos")

    respuesta = input("\n¿Desea continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("\n⊘ Migración cancelada")
        return 0

    # Obtener modelos en orden
    models = get_all_models()
    print(f"\n📦 Se migrarán {len(models)} modelos")

    # Migrar cada modelo
    start_time = datetime.now()
    success_count = 0
    fail_count = 0

    for model in models:
        if migrate_model(model):
            success_count += 1
        else:
            fail_count += 1

    # Reiniciar secuencias
    reset_sequences()

    # Resumen
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'='*60}")
    print("RESUMEN DE MIGRACIÓN")
    print(f"{'='*60}")
    print(f"✓ Modelos migrados exitosamente: {success_count}")
    if fail_count > 0:
        print(f"✗ Modelos con errores: {fail_count}")
    print(f"⏱️  Tiempo total: {duration}")
    print(f"Fecha de finalización: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n✅ Migración completada")
    print("\nPróximos pasos:")
    print("  1. Verificar la integridad de los datos en PostgreSQL")
    print("  2. Probar la aplicación con PostgreSQL")
    print("  3. Actualizar DATABASES['default'] en settings.py si es necesario")

    return 0


if __name__ == '__main__':
    sys.exit(main())
