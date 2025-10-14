
Manual para Desarrolladores: Instalación y Dominio de django-unfold


Introducción: Modernizando el Admin de Django con Unfold

django-unfold es más que un simple tema; es un conjunto de herramientas integral diseñado para transformar el panel de administración por defecto de Django en una interfaz administrativa moderna, potente y amigable para el desarrollador.1 Como proyecto de código abierto, su objetivo principal es resolver los problemas comunes de UI/UX inherentes al panel de administración estándar, ofreciendo una experiencia pulida y eficiente desde el primer momento.3

Tecnologías Centrales

La modernidad y el rendimiento de Unfold se basan en un conjunto de tecnologías de front-end de primer nivel. Utiliza Tailwind CSS, un framework CSS de tipo "utility-first" que permite una estilización rápida y personalizable.1 Para la interactividad, se apoya en
Alpine.js, una biblioteca de JavaScript ligera que facilita la manipulación reactiva y declarativa del DOM, y en HTMX, que permite interacciones AJAX fluidas entre el navegador y el servidor utilizando atributos HTML simples.1 Esta base tecnológica es la fuente de su apariencia moderna, su capacidad de respuesta y su rendimiento.

Propuesta de Valor

Los beneficios de adoptar Unfold sobre el panel de administración por defecto son significativos. Ofrece una interfaz completamente responsiva que funciona a la perfección en todos los dispositivos, una mejora sustancial sobre el diseño parcialmente responsivo de Django.5 Además, introduce características avanzadas que normalmente requerirían un desarrollo considerable, como dashboards personalizables, un sistema de filtros mejorado, una biblioteca de componentes de UI reutilizables y soporte nativo para modo claro y oscuro.1 Estas capacidades posicionan a Unfold como una opción estratégica para cualquier desarrollador de Django que busque mejorar la productividad y la experiencia de usuario final.

Sección 1: Instalación y Configuración Fundamentales

Una implementación exitosa de django-unfold depende de una configuración inicial precisa. Esta sección detalla cada paso, explicando la lógica subyacente para prevenir los errores más comunes.

1.1. Prerrequisitos y Buenas Prácticas del Entorno

Antes de la instalación, es fundamental seguir las mejores prácticas de desarrollo en Django. Se recomienda encarecidamente el uso de entornos virtuales (utilizando herramientas como venv, pipenv o poetry) para aislar las dependencias del proyecto. Esta práctica previene conflictos entre paquetes y es crucial para un entorno de desarrollo limpio y reproducible.7
django-unfold requiere una versión de Python 3.9 o superior.6

1.2. Instalación del Paquete

La instalación de django-unfold se puede realizar a través de los gestores de paquetes de Python más populares. Los comandos, listos para ser copiados y pegados, son los siguientes 8:
Con pip:
Bash
pip install django-unfold


Con poetry:
Bash
poetry add django-unfold


Con uv:
Bash
uv add django-unfold


Es importante no confundir este paquete con otros de nombre similar en PyPI. Por ejemplo, django-unfold-admin es un fork que añade soporte para RTL (de derecha a izquierda) 11, mientras que
unfold es un paquete completamente diferente relacionado con el análisis del ciclo de vida (LCA).12 Instalar el paquete incorrecto es una fuente común de errores.

1.3. Configuración Central del Proyecto: settings.py y INSTALLED_APPS

El paso de configuración más crítico reside en el archivo settings.py de su proyecto. Es imperativo añadir la aplicación 'unfold' a la lista INSTALLED_APPS.
Este paso no es una simple formalidad; la posición de 'unfold' en esta lista determina su funcionamiento. Django procesa la lista INSTALLED_APPS de forma secuencial para descubrir plantillas, archivos estáticos y otros recursos. Al colocar 'unfold' antes de 'django.contrib.admin', se asegura que el cargador de plantillas de Django encuentre y utilice primero las plantillas de Unfold, que están diseñadas para sobreescribir las del panel de administración por defecto. Si se colocara después, Django cargaría sus propias plantillas, y la interfaz de Unfold no se aplicaría, resultando en un panel sin estilos o con un funcionamiento incorrecto.13 Esta arquitectura de sobreescritura de plantillas es fundamental para el funcionamiento de Unfold y es la causa principal de muchos problemas de visualización iniciales.
La configuración correcta se ve así 5:

Python


# settings.py
INSTALLED_APPS =


Unfold también proporciona módulos contrib opcionales que extienden su funcionalidad, como unfold.contrib.filters para filtros avanzados o unfold.contrib.forms para widgets de formulario personalizados.8

1.4. La Herencia Crítica de ModelAdmin en admin.py

Para que los estilos y las funcionalidades de Unfold se apliquen a las páginas de administración de un modelo específico, la clase ModelAdmin correspondiente debe heredar de unfold.admin.ModelAdmin en lugar de la clase estándar django.contrib.admin.ModelAdmin.8
Omitir este paso es un error común que resulta en formularios sin estilo y en la ausencia de las características avanzadas de Unfold dentro de las vistas de detalle y listado de ese modelo.8
El siguiente ejemplo de código ilustra la implementación correcta:

Python


# en el archivo admin.py de tu aplicación
from django.contrib import admin
from.models import MyModel
from unfold.admin import ModelAdmin  # Importación clave

@admin.register(MyModel)
class CustomAdminClass(ModelAdmin):  # Heredar de ModelAdmin de Unfold
    pass



1.5. Manejo de los Modelos por Defecto de Usuario y Grupo de Django

Un caso de uso particular que requiere atención es la gestión de los modelos User y Group de Django. Estos son registrados automáticamente por django.contrib.auth utilizando el ModelAdmin estándar, lo que provoca que aparezcan sin los estilos de Unfold.15
La solución oficial consiste en desregistrar las clases de administración por defecto y volver a registrarlas utilizando una clase personalizada que herede tanto de la clase base de Django (BaseUserAdmin, BaseGroupAdmin) como de unfold.admin.ModelAdmin. Adicionalmente, es necesario especificar los formularios personalizados de Unfold para asegurar una integración visual completa.9

Python


# en un archivo admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

# Desregistrar los modelos por defecto
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Formularios cargados desde unfold.forms para un estilo consistente
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass



1.6. Verificación Inicial y Gestión de Archivos Estáticos (collectstatic)

El último paso de la configuración inicial es ejecutar el comando python manage.py collectstatic. Este comando es esencial para entornos de producción, ya que recopila todos los archivos estáticos (CSS, JavaScript, imágenes) de todas las aplicaciones instaladas, incluyendo Unfold, y los agrupa en un único directorio definido por STATIC_ROOT.13
Aunque el servidor de desarrollo de Django (runserver) gestiona los archivos estáticos automáticamente cuando DEBUG=True, ejecutar collectstatic es un paso obligatorio para cualquier despliegue en producción y una buena práctica para verificar que todos los recursos se localizan correctamente.

Sección 2: Configuración Esencial y Personalización de Marca

Una vez completada la instalación básica, el siguiente paso es personalizar el panel de administración para que se alinee con la identidad visual y los requisitos del proyecto.

2.1. El Diccionario UNFOLD: Un Panel de Control Centralizado

La mayoría de las personalizaciones de alto nivel de Unfold se gestionan a través de un diccionario llamado UNFOLD en el archivo settings.py.5 Este diccionario actúa como un panel de control central para configurar el comportamiento y la apariencia del panel de administración.
Una configuración mínima para empezar podría ser la siguiente 5:

Python


# settings.py
UNFOLD = {
    "SITE_TITLE": "Panel de Administración de Mi Proyecto",
    "SITE_HEADER": "Mi Proyecto",
    "SHOW_HISTORY": True,  # Muestra el historial de acciones recientes en el dashboard
    "DARK_MODE": True,  # Habilita el soporte para modo oscuro
    "SIDEBAR": {
        "show_search": True,  # Muestra la barra de búsqueda en el menú lateral
        "show_all_applications": True,  # Muestra un enlace para ver todas las aplicaciones
    }
}


La siguiente tabla resume algunas de las opciones de configuración más importantes disponibles en el diccionario UNFOLD, sirviendo como una referencia rápida para los desarrolladores.
Tabla 1: El Diccionario de Configuración UNFOLD
Clave
Tipo de Dato
Propósito
Ejemplo
SITE_TITLE
str
Establece el texto en la etiqueta <title> del navegador.
'Admin de Mi Proyecto'
SITE_HEADER
str
El texto principal que aparece en la parte superior del menú lateral.
'Mi Proyecto'
SITE_LOGO
dict o lambda
Define la ruta al logo del sitio para los modos claro y oscuro.
{'light': lambda r: static('logo-claro.svg'), 'dark': lambda r: static('logo-oscuro.svg')}
SITE_ICON
dict o lambda
Define la ruta al favicon del sitio.
lambda request: static('favicon.ico')
DARK_MODE
bool
Habilita o deshabilita el soporte para el modo oscuro.
True
SIDEBAR
dict
Configura el comportamiento del menú lateral (búsqueda, lista de apps).
{'show_search': True, 'show_all_applications': True}
STYLES
list
Una lista de rutas a archivos CSS adicionales para cargar.
[lambda request: static('css/custom_admin.css')]
SCRIPTS
list
Una lista de rutas a archivos JavaScript adicionales para cargar.
[lambda request: static('js/custom_admin.js')]
DASHBOARD_CALLBACK
str
Ruta a una función para inyectar datos en el dashboard principal.
'mi_app.utils.dashboard_callback'


2.2. Personalización de la Marca del Panel

Para alinear el panel de administración con la identidad visual de una marca, se pueden utilizar varias claves dentro del diccionario UNFOLD. Las claves SITE_TITLE, SITE_HEADER, SITE_LOGO y SITE_ICON permiten un control detallado sobre los elementos visuales más prominentes del panel.18

2.3. Configuración de la Navegación Lateral

El menú lateral es un componente central de la navegación. La clave SIDEBAR dentro del diccionario UNFOLD permite configurar su comportamiento, como mostrar u ocultar la barra de búsqueda y el enlace para ver todas las aplicaciones, mejorando la usabilidad para los administradores.3

2.4. Temas y Apariencia

Unfold facilita la personalización de la apariencia visual. La clave DARK_MODE permite habilitar un tema oscuro con un solo ajuste.5 Para personalizaciones más profundas, las opciones de temas permiten cambiar la paleta de colores para que coincida con la identidad de la marca.1 Para aquellos que prefieren una solución sin código,
Unfold Studio es una herramienta premium que ofrece un personalizador visual para ajustar colores, logos y estilos de la interfaz de forma intuitiva.1

Sección 3: Integración con el Ecosistema de Django

Unfold está diseñado para integrarse fluidamente con otros paquetes populares del ecosistema de Django, mejorando sus funcionalidades con una interfaz de usuario consistente.

3.1. El Patrón General para la Integración de Paquetes de Terceros

La integración con paquetes soportados sigue un patrón de diseño deliberado y predecible. Unfold encapsula las personalizaciones necesarias (como la sobreescritura de plantillas y la lógica de ModelAdmin) en módulos específicos bajo el espacio de nombres unfold.contrib. Este enfoque, conocido como el "patrón de encapsulación contrib", simplifica enormemente el proceso para el desarrollador. La integración típicamente requiere tres pasos:
Añadir el módulo unfold.contrib.<nombre_del_paquete> a INSTALLED_APPS.
Asegurar que el orden de carga sea el correcto (generalmente antes del paquete original).
Realizar los ajustes necesarios en la clase ModelAdmin, como heredar de una clase mixta o configurar atributos específicos.
Este diseño no solo facilita las integraciones soportadas, sino que también proporciona un modelo mental claro para los desarrolladores que deseen integrar paquetes no soportados oficialmente, ya que pueden replicar este patrón creando sus propias plantillas y clases mixin.

3.2. Guías de Integración Paso a Paso

A continuación se detallan los pasos para integrar Unfold con algunos de los paquetes más comunes.

Gestión de Datos con django-import-export

Para integrar las potentes funcionalidades de importación y exportación de datos, se deben seguir estos pasos 8:
Añadir 'unfold.contrib.import_export' a INSTALLED_APPS.
En la clase ModelAdmin que hereda de ImportExportModelAdmin, especificar los atributos import_form_class y export_form_class proporcionados por Unfold. Esto asegura que los formularios de importación y exportación adopten el estilo de Unfold.
Unfold proporciona una demostración en vivo de esta integración para referencia visual.19

Auditoría con django-simple-history

Para visualizar el historial de cambios de los modelos con una interfaz moderna 20:
Añadir 'unfold.contrib.simple_history' a INSTALLED_APPS, asegurándose de que se encuentre después de 'unfold' pero antes de 'simple_history'.
En la clase ModelAdmin del modelo auditado, heredar tanto de SimpleHistoryAdmin como de unfold.admin.ModelAdmin.

Permisos con django-guardian

Para gestionar permisos a nivel de objeto directamente desde el panel de administración 21:
Añadir 'unfold.contrib.guardian' a INSTALLED_APPS.
Este único paso es suficiente para sobreescribir las plantillas necesarias y añadir un botón de "Permisos de objeto" en el formulario de cambio del modelo.

3.3. Notas sobre Otras Integraciones Clave

Unfold también ofrece soporte oficial para otros paquetes populares, como django-celery-beat para la gestión de tareas periódicas y django-constance para la configuración dinámica, demostrando su compromiso con la compatibilidad dentro del ecosistema de Django.1

Sección 4: Implementación Avanzada: Dashboards y Componentes Personalizados

Más allá de la configuración básica, Unfold proporciona las herramientas para construir experiencias administrativas verdaderamente personalizadas.

4.1. Construyendo una Página de Dashboard Personalizada

Crear un dashboard a medida es una de las personalizaciones más potentes. El proceso, documentado en el blog oficial y demostrado en el repositorio formula, implica los siguientes pasos 22:
Sobrescribir la Plantilla Principal: Crear un archivo admin/index.html en el directorio de plantillas de su proyecto para reemplazar el dashboard por defecto.
Inyectar Datos Personalizados: Utilizar la clave DASHBOARD_CALLBACK en el diccionario UNFOLD de settings.py. Esta clave debe apuntar a una función en su código (por ejemplo, 'mi_app.utils.dashboard_callback').
Crear la Función de Callback: Esta función recibe el objeto request y un diccionario de context como argumentos. Se pueden añadir datos personalizados a este contexto, que luego estarán disponibles en la plantilla admin/index.html.23

4.2. Aprovechando la Biblioteca de Componentes Reutilizables de Unfold

Unfold incluye una biblioteca de componentes de UI pre-estilizados, como tarjetas, botones y gráficos, que permiten construir páginas personalizadas rápidamente y sin necesidad de escribir CSS extenso.1 Estos componentes se pueden invocar directamente desde las plantillas, como se muestra en el blog oficial, para crear diseños complejos y consistentes con el resto del panel de administración.23

4.3. Utilizando Funcionalidades Avanzadas de ModelAdmin

Al heredar de unfold.admin.ModelAdmin, se desbloquean varias funcionalidades avanzadas para organizar y mejorar los formularios de administración:
Pestañas para Fieldsets (fieldset_tabs): Permite agrupar múltiples fieldsets en una interfaz de pestañas, mejorando la organización de formularios largos.1
Pestañas para Inlines (inline_tabs): De manera similar, agrupa múltiples inlines en pestañas, limpiando la vista de cambio.2
Campos Condicionales: Permite mostrar u ocultar campos de un formulario dinámicamente en función de los valores de otros campos, creando formularios más inteligentes e intuitivos.1

4.4. Incorporando Estilos y Scripts Personalizados a Nivel de Proyecto

Para una personalización más profunda, se pueden añadir archivos CSS y JavaScript específicos del proyecto. Esto se logra utilizando las claves STYLES y SCRIPTS en el diccionario UNFOLD.9 Para asegurar que los estilos personalizados sean consistentes con el sistema de diseño de Unfold, se puede configurar un archivo
tailwind.config.js en el proyecto. Esto permite compilar CSS personalizado que utiliza las mismas utilidades y tokens de diseño que Unfold, garantizando una integración visual perfecta.9

Sección 5: Solución de Problemas y Despliegue en Producción

Esta sección ofrece una guía práctica para diagnosticar y resolver los problemas más frecuentes que los desarrolladores encuentran durante la implementación y el despliegue.

5.1. Diagnóstico de Problemas Comunes de Estilo: El Problema del "Admin sin Estilos"

El problema más recurrente es un panel de administración que aparece completamente sin estilos. Este inconveniente, especialmente en producción, casi nunca es un error en django-unfold. En cambio, actúa como una prueba de fuego para la configuración de despliegue de Django. Dado que Unfold depende en gran medida de sus recursos estáticos (CSS y JavaScript), cualquier fallo en la cadena de servicio de estos archivos se hace inmediatamente visible. Un panel de administración de Django estándar podría parecer parcialmente funcional con archivos estáticos rotos, pero Unfold se mostrará completamente inutilizable.
Este comportamiento convierte a Unfold en una herramienta de diagnóstico involuntaria pero muy eficaz: si el panel de Unfold no tiene estilos en producción, es una señal inequívoca de que la configuración de los archivos estáticos del proyecto es incorrecta. La solución pasa por revisar los fundamentos del despliegue en Django, una habilidad crucial para cualquier desarrollador.
Para diagnosticar este problema, se debe seguir la siguiente lista de verificación 13:
Verificar INSTALLED_APPS: ¿Está 'unfold' como la primera entrada en la lista?
Verificar la Herencia de ModelAdmin: ¿Todas las clases ModelAdmin relevantes heredan de unfold.admin.ModelAdmin?
Ejecutar collectstatic: En un entorno de producción (DEBUG=False), ¿se ha ejecutado el comando python manage.py collectstatic?
Configuración del Servidor Web: ¿Está el servidor web (por ejemplo, Nginx) configurado correctamente para servir los archivos desde el directorio STATIC_ROOT en la URL definida por STATIC_URL?

5.2. Resolución de Conflictos con Paquetes de Terceros

Si un paquete de terceros no tiene un módulo contrib oficial y aparece sin estilos, la solución general es aplicar el patrón de unregister/re-register. Esto implica desregistrar el ModelAdmin por defecto del paquete y volver a registrar el modelo con una clase personalizada que herede tanto del ModelAdmin original del paquete como de unfold.admin.ModelAdmin.9 Esta técnica es una solución potente y versátil para garantizar la consistencia visual.

5.3. Mejores Prácticas para el Despliegue en Producción

Para un despliegue exitoso, es fundamental comprender cómo Django maneja los archivos estáticos:
DEBUG=False: En producción, esta configuración deshabilita el servicio de archivos estáticos por parte de Django, ya que es ineficiente y no seguro.16
collectstatic: Este comando debe ejecutarse durante el proceso de despliegue para reunir todos los archivos estáticos en la ubicación STATIC_ROOT.13
Servidor Web: Un servidor web como Nginx debe ser configurado para interceptar las peticiones a STATIC_URL y servir los archivos directamente desde el directorio STATIC_ROOT en el sistema de archivos.17

5.4. Búsqueda de Asistencia Adicional

Si los problemas persisten, la comunidad y los mantenedores de Unfold ofrecen varios canales de ayuda:
Paquetes de Soporte Oficial: Para problemas críticos de negocio, se ofrecen paquetes de soporte profesional que incluyen consultoría y revisiones de implementación.1
GitHub Issues: Para reportar errores o problemas técnicos específicos, el rastreador de incidencias de GitHub es el canal adecuado.28
Comunidad de Discord: Para discusiones, preguntas generales y ayuda de la comunidad, el servidor oficial de Discord es un recurso valioso.1

Conclusión: El Impacto Transformador de una Interfaz de Administración Moderna

En resumen, django-unfold es una herramienta poderosa que, cuando se instala y configura correctamente, mejora drásticamente la experiencia tanto para los desarrolladores como para los usuarios finales. Su implementación exitosa depende de comprender algunos conceptos clave de Django, como el orden de las aplicaciones y la gestión de archivos estáticos. Al seguir los pasos descritos en esta guía, los desarrolladores pueden superar los obstáculos comunes y aprovechar todo el potencial de Unfold para crear paneles de administración que no solo son funcionales, sino también modernos, intuitivos y altamente personalizables. El resultado final es un producto de mayor calidad y un proceso de desarrollo más eficiente.

Apéndice: Recursos Esenciales

Documentación Oficial: unfoldadmin.com 1
Demostración en Vivo: demo.unfoldadmin.com 13
Repositorio de Demostración (Formula): github.com/unfoldadmin/formula (Un ejemplo completo de implementación) 1
Boilerplate (Turbo): github.com/unfoldadmin/turbo (Un proyecto de inicio con Django y Next.js) 1
Comunidad de Discord: Enlace disponible en la documentación oficial 1
Repositorio de GitHub: github.com/unfoldadmin/django-unfold 2
Fuentes citadas
django-unfold - PyPI, acceso: septiembre 5, 2025, https://pypi.org/project/django-unfold/
unfoldadmin/django-unfold: Modern Django admin theme - GitHub, acceso: septiembre 5, 2025, https://github.com/unfoldadmin/django-unfold
Admin theme for Django - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/
Django tip Customize Your Django Admin with django-unfold - Reddit, acceso: septiembre 5, 2025, https://www.reddit.com/r/django/comments/1kruwht/django_tip_customize_your_django_admin_with/
Getting Started with Django Unfold: A Modern UI for Django Admin - Medium, acceso: septiembre 5, 2025, https://medium.com/django-unleashed/getting-started-with-django-unfold-a-modern-ui-for-django-admin-aeb8be63bd0a
django-unfold - PyDigger, acceso: septiembre 5, 2025, https://pydigger.com/pypi/django-unfold
Common issues and pitfalls new django users fall into. - Reddit, acceso: septiembre 5, 2025, https://www.reddit.com/r/django/comments/1976662/common_issues_and_pitfalls_new_django_users_fall/
Quickstart - Unfold - Admin theme for Django, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/installation/quickstart/
django-unfold 0.5.0 - PyPI, acceso: septiembre 5, 2025, https://pypi.org/project/django-unfold/0.5.0/
django-unfold - PyPI, acceso: septiembre 5, 2025, https://pypi.org/project/django-unfold/0.3.0/
django-unfold-admin - pypi Package Security Analysis - Socke... - Socket.dev, acceso: septiembre 5, 2025, https://socket.dev/pypi/package/django-unfold-admin
unfold - PyPI, acceso: septiembre 5, 2025, https://pypi.org/project/unfold/
Unfold admin theme documentation, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/
ModelAdmin options - Django - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/configuration/modeladmin/
User & group models - Django - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/installation/auth/
Django Static files 404 - Stack Overflow, acceso: septiembre 5, 2025, https://stackoverflow.com/questions/12809416/django-static-files-404
How to solve 404 for static files with Django and Nginx? - Ask Ubuntu, acceso: septiembre 5, 2025, https://askubuntu.com/questions/477271/how-to-solve-404-for-static-files-with-django-and-nginx
Settings options - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/configuration/settings/
django-import-export - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/integrations/django-import-export/
django-simple-history - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/integrations/django-simple-history/
django-guardian - Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/docs/integrations/django-guardian/
unfoldadmin/formula: Unfold Django admin theme demo repository for demonstration purposes implementing various admin possibilities - GitHub, acceso: septiembre 5, 2025, https://github.com/unfoldadmin/formula
Turn Django admin into full-fledged dashboard with Unfold, acceso: septiembre 5, 2025, https://unfoldadmin.com/blog/django-admin-dashboard-unfold/
Admin Panel is not styled in unfold when production when serving ..., acceso: septiembre 5, 2025, https://www.reddit.com/r/django/comments/1lwebjr/admin_panel_is_not_styled_in_unfold_when/
Static files returns 404 when debug is set to False - django - Reddit, acceso: septiembre 5, 2025, https://www.reddit.com/r/django/comments/11hv657/static_files_returns_404_when_debug_is_set_to/
django-unfold - PyPI, acceso: septiembre 5, 2025, https://pypi.org/project/django-unfold/0.6.2/
Unfold support package, acceso: septiembre 5, 2025, https://unfoldadmin.com/support/
Django Admin Unfold - Reddit, acceso: septiembre 5, 2025, https://www.reddit.com/r/django/comments/1jqm8x8/django_admin_unfold/
Issues · unfoldadmin/django-unfold - GitHub, acceso: septiembre 5, 2025, https://github.com/unfoldadmin/django-unfold/issues
unfoldadmin - GitHub, acceso: septiembre 5, 2025, https://github.com/unfoldadmin
