#!/usr/bin/env python
"""
Script de prueba para verificar el funcionamiento de la interfaz RRHH
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
django.setup()

from apps.reloj_fichador.models import Area, Operario
from django.db.models import Count, Q

def test_queries():
    """Prueba las consultas que estaban fallando"""
    print("=== PRUEBA DE CONSULTAS ===")
    
    # Probar consulta de áreas
    try:
        areas_data = Area.objects.annotate(
            total_operarios=Count('operario_set', filter=Q(operario_set__activo=True))
        ).filter(total_operarios__gt=0)
        print(f"✅ Consulta de áreas exitosa: {areas_data.count()} áreas con operarios activos")
        for area in areas_data[:3]:  # Solo los primeros 3
            print(f"  - {area.nombre}: {area.total_operarios} operarios")
    except Exception as e:
        print(f"❌ Error en consulta de áreas: {e}")
        return False
    
    # Probar datos básicos
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  - Total áreas: {Area.objects.count()}")
    print(f"  - Total operarios: {Operario.objects.count()}")
    print(f"  - Operarios activos: {Operario.objects.filter(activo=True).count()}")
    
    return True

def test_rrhh_view():
    """Prueba el acceso a la vista RRHH"""
    print("\n=== PRUEBA DE VISTA RRHH ===")
    
    # Crear cliente
    client = Client()
    
    # Obtener superusuario
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("❌ No hay superusuarios disponibles")
        return False
    
    print(f"🔐 Usuario de prueba: {user.username}")
    
    # Forzar login
    client.force_login(user)
    
    # Probar acceso al dashboard
    try:
        response = client.get('/rrhh/')
        print(f"📄 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dashboard RRHH carga correctamente")
            return True
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error al acceder a dashboard: {e}")
        return False

if __name__ == "__main__":
    print("🧪 PROBANDO INTERFAZ RRHH\n")
    
    queries_ok = test_queries()
    view_ok = test_rrhh_view()
    
    print(f"\n📋 RESULTADO:")
    print(f"  - Consultas: {'✅ OK' if queries_ok else '❌ ERROR'}")
    print(f"  - Vista RRHH: {'✅ OK' if view_ok else '❌ ERROR'}")
    
    if queries_ok and view_ok:
        print("\n🎉 ¡Todo funciona correctamente!")
        sys.exit(0)
    else:
        print("\n⚠️  Hay problemas que necesitan atención")
        sys.exit(1)
