from django.contrib import admin
from .models import Operario, Entrada, SalidaTra, EntradaTra, Salida, HorasMensual

admin.site.register(Operario)
admin.site.register(Entrada)
admin.site.register(SalidaTra)
admin.site.register(EntradaTra)
admin.site.register(Salida)
admin.site.register(HorasMensual)

