from __future__ import annotations

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.reloj_fichador.models import CalendarioLaboral, SugerenciaFeriado
from apps.reloj_fichador.utils import obtener_feriados_api


class Command(BaseCommand):
    help = "Sincroniza feriados desde la API ArgentinaDatos y crea sugerencias para ser revisadas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            "--año",
            dest="years",
            type=int,
            nargs="+",
            help="Año(s) a sincronizar. Por defecto se sincroniza el año actual y el siguiente.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Actualiza información de sugerencias ya existentes.",
        )
        parser.add_argument(
            "--solo-pendientes",
            action="store_true",
            help="Solo muestra resumen de sugerencias pendientes sin consultar la API.",
        )

    def handle(self, *args, **options):
        if options.get("solo_pendientes"):
            return self._mostrar_pendientes()

        years = options.get("years")
        if not years:
            año_actual = timezone.now().year
            years = [año_actual, año_actual + 1]

        force_update = options.get("force", False)

        total_creadas = 0
        total_actualizadas = 0
        total_existentes = 0

        for año in years:
            self.stdout.write(self.style.MIGRATE_HEADING(f"Sincronizando feriados para {año}"))
            feriados = obtener_feriados_api(año)

            if not feriados:
                self.stderr.write(self.style.WARNING(f"No se obtuvieron feriados para {año}."))
                continue

            fechas_calendario = set(
                CalendarioLaboral.objects.filter(fecha__year=año).values_list("fecha", flat=True)
            )
            sugerencias_existentes = {
                (s.fecha, s.fuente): s
                for s in SugerenciaFeriado.objects.filter(fecha__year=año)
            }

            for feriado in feriados:
                fecha = feriado.get("fecha")
                nombre = feriado.get("nombre")
                tipo = feriado.get("tipo_sugerencia")

                if not isinstance(fecha, date):
                    self.stderr.write(self.style.WARNING(f"Fecha inválida recibida: {fecha!r}"))
                    continue

                if fecha in fechas_calendario:
                    total_existentes += 1
                    self.stdout.write(
                        self.style.NOTICE(
                            f"- {fecha} ya está registrado en CalendarioLaboral como día especial."
                        )
                    )
                    continue

                clave = (fecha, "api_argentina")
                sugerencia = sugerencias_existentes.get(clave)

                if sugerencia:
                    if force_update:
                        sugerencia.nombre = nombre
                        sugerencia.tipo_sugerencia = tipo
                        sugerencia.datos_fuente = feriado.get("datos_originales")
                        sugerencia.fuente_url = feriado.get("fuente_url")
                        sugerencia.estado = "pendiente" if sugerencia.estado == "pendiente" else sugerencia.estado
                        sugerencia.save(update_fields=["nombre", "tipo_sugerencia", "datos_fuente", "fuente_url", "estado"])
                        total_actualizadas += 1
                    else:
                        self.stdout.write(
                            self.style.NOTICE(
                                f"- {fecha} ya tiene una sugerencia registrada (estado: {sugerencia.get_estado_display()})."
                            )
                        )
                    continue

                with transaction.atomic():
                    SugerenciaFeriado.objects.create(
                        fecha=fecha,
                        nombre=nombre,
                        tipo_sugerencia=tipo,
                        fuente="api_argentina",
                        datos_fuente=feriado.get("datos_originales"),
                        fuente_url=feriado.get("fuente_url"),
                    )
                total_creadas += 1
                self.stdout.write(self.style.SUCCESS(f"+ Sugerencia creada para {fecha}: {nombre}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Sincronización completada"))
        self.stdout.write(self.style.SUCCESS(f"  ➕ Sugerencias nuevas: {total_creadas}"))
        if force_update:
            self.stdout.write(self.style.SUCCESS(f"  🔄 Sugerencias actualizadas: {total_actualizadas}"))
        self.stdout.write(self.style.SUCCESS(f"  ✅ Ya existentes en calendario: {total_existentes}"))

        return 0

    def _mostrar_pendientes(self):
        pendientes = SugerenciaFeriado.objects.filter(estado="pendiente").order_by("fecha")
        if not pendientes.exists():
            self.stdout.write(self.style.SUCCESS("No hay sugerencias de feriados pendientes."))
            return 0

        self.stdout.write(self.style.MIGRATE_LABEL("Sugerencias de feriados pendientes:"))
        for sug in pendientes:
            estado_calendario = "✅ ya registrado" if sug.ya_existe_en_calendario else "⏳ pendiente"
            self.stdout.write(
                f"- {sug.fecha:%d/%m/%Y} · {sug.nombre} · {sug.get_tipo_sugerencia_display()} ({estado_calendario})"
            )
        self.stdout.write(self.style.NOTICE(f"Total pendientes: {pendientes.count()}"))
        return 0
