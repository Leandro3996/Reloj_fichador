"""
Comando Django para sincronizar feriados desde la API ArgentinaDatos.

Uso:
    python manage.py sincronizar_feriados              # Usa año actual
    python manage.py sincronizar_feriados 2025
    python manage.py sincronizar_feriados 2025 --aceptar-todos
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime
from apps.reloj_fichador.models import SugerenciaFeriado, CalendarioLaboral
from apps.reloj_fichador.utils import obtener_feriados_api
import logging

logger = logging.getLogger('reloj_fichador')


class Command(BaseCommand):
    help = 'Sincroniza feriados desde la API ArgentinaDatos y crea sugerencias'

    def add_arguments(self, parser):
        parser.add_argument(
            'año',
            type=int,
            nargs='?',  # Argumento opcional
            default=None,
            help='Año para el cual obtener feriados (default: año actual)'
        )
        parser.add_argument(
            '--aceptar-todos',
            action='store_true',
            help='Acepta automáticamente todas las sugerencias'
        )
        parser.add_argument(
            '--limpiar-pendientes',
            action='store_true',
            help='Elimina sugerencias pendientes antes de sincronizar'
        )

    def handle(self, *args, **options):
        año = options['año'] or timezone.now().year
        aceptar_todos = options.get('aceptar_todos', False)
        limpiar_pendientes = options.get('limpiar_pendientes', False)

        self.stdout.write(f"\n📅 Sincronizando feriados para {año}...\n")

        try:
            # Limpiar pendientes si se solicita
            if limpiar_pendientes:
                pendientes = SugerenciaFeriado.objects.filter(estado='pendiente')
                count = pendientes.count()
                pendientes.delete()
                self.stdout.write(self.style.WARNING(f"⚠️  Eliminadas {count} sugerencias pendientes\n"))

            # Obtener feriados de la API
            feriados_api = obtener_feriados_api(año)

            if not feriados_api:
                self.stdout.write(
                    self.style.ERROR(
                        "❌ No se pudieron obtener feriados de la API. "
                        "Verifica tu conexión a internet.\n"
                    )
                )
                return

            self.stdout.write(f"✅ Se obtuvieron {len(feriados_api)} feriados de la API\n")

            # Procesar cada feriado
            nuevas_sugerencias = 0
            ya_existentes = 0
            ya_aceptadas = 0

            for feriado_dict in feriados_api:
                try:
                    fecha = feriado_dict['fecha']
                    nombre = feriado_dict['nombre']
                    tipo = feriado_dict['tipo_sugerencia']

                    # Verificar si ya existe en CalendarioLaboral
                    if CalendarioLaboral.objects.filter(
                        fecha=fecha,
                        tipo_dia__in=['feriado', 'feriado_movible']
                    ).exists():
                        ya_aceptadas += 1
                        self.stdout.write(
                            f"  ⏭️  {fecha} - {nombre} (ya aceptado en calendario)"
                        )
                        continue

                    # Crear o actualizar sugerencia
                    sugerencia, creada = SugerenciaFeriado.objects.get_or_create(
                        fecha=fecha,
                        fuente='api_argentina',
                        defaults={
                            'nombre': nombre,
                            'tipo_sugerencia': tipo,
                            'estado': 'pendiente' if not aceptar_todos else 'aceptado',
                        }
                    )

                    if creada:
                        nuevas_sugerencias += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✨ {fecha} - {nombre} (nueva)")
                        )

                        # Si --aceptar-todos, acepta automáticamente
                        if aceptar_todos:
                            sugerencia.aceptar()
                            self.stdout.write(
                                self.style.SUCCESS(f"     ✅ Aceptada automáticamente")
                            )
                    else:
                        self.stdout.write(
                            f"  ℹ️  {fecha} - {nombre} (ya existía como sugerencia)"
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  ❌ Error procesando feriado: {str(e)}")
                    )
                    logger.error(f"Error en sincronizar_feriados: {str(e)}")

            # Resumen
            self.stdout.write("\n" + "=" * 70)
            self.stdout.write("📊 RESUMEN DE SINCRONIZACIÓN:\n")
            self.stdout.write(f"  ✨ Nuevas sugerencias creadas: {nuevas_sugerencias}")
            self.stdout.write(f"  ✅ Ya aceptadas en calendario: {ya_aceptadas}")
            self.stdout.write(f"  ℹ️  Ya existían como sugerencias: {len(feriados_api) - nuevas_sugerencias - ya_aceptadas}")

            if aceptar_todos and nuevas_sugerencias > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"\n  🎉 {nuevas_sugerencias} feriados aceptados automáticamente")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"\n  ⏳ {nuevas_sugerencias} sugerencias pendientes de revisión")
                )

            self.stdout.write("=" * 70 + "\n")
            self.stdout.write(
                self.style.SUCCESS("✅ Sincronización completada exitosamente\n")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error durante la sincronización: {str(e)}\n")
            )
            logger.error(f"Error en sincronizar_feriados: {str(e)}")
            raise CommandError(f"Error al sincronizar feriados: {str(e)}")
