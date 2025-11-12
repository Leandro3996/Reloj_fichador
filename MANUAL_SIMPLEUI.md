
Manual de Implementación y Configuración de Django SimpleUI

A continuación, se presenta un manual técnico exhaustivo para la implementación y configuración de la biblioteca django-simpleui. Este documento se basa en el análisis de la documentación oficial del proyecto y está diseñado para guall a los desarrolladores en la correcta instalación, personalización y despliegue, asegurando la integridad funcional y estética del panel de administración de Django.

Sección I: Introducción, Instalación y Análisis de Compatibilidad

Esta sección establece los fundamentos del proyecto, su instalación y aborda el punto crítico de la compatibilidad de versiones para prevenir conflictos en el despliegue.

1.1 Propósito y Alcance del Manual

El propósito de este documento es proporcionar una guía de referencia completa en español para la biblioteca django-simpleui, un popular tema para el panel de administración de Django.1 El objetivo es permitir a los desarrolladores configurar el paquete de manera que funcione correctamente, sin pérdida de estética o funcionalidad, y evitando incompatibilidades.
Es fundamental diferenciar el alcance de este manual. La documentación analizada 1 y los repositorios de código asociados 2 indican la existencia de dos versiones:
SimpleUI (Gratuita): El proyecto django-simpleui analizado en este manual. Es un tema que se instala sobre el admin de Django existente para modernizar su interfaz.2
SimplePro (Versión Profesional): Un producto comercial separado que, según la descripción, ofrece una arquitectura de separación entre frontend y backend, más funciones y una interfaz diferente.3
Este manual cubre exclusivamente la biblioteca gratuita django-simpleui. Las configuraciones y características de SimplePro no se abordan y no son compatibles con los parámetros aquí descritos.

1.2 Instalación e Integración

La instalación de django-simpleui sigue el procedimiento estándar de las aplicaciones de Django.
Paso 1: Instalación del Paquete
Utilice pip para instalar el paquete desde el Python Package Index (PyPI) 4:

Bash


pip install django-simpleui


Paso 2: Configuración en settings.py
Para que Django reconozca y utilice simpleui, la aplicación debe registrarse en el archivo settings.py del proyecto. Debe añadirse a la lista INSTALLED_APPS.
Para un funcionamiento correcto, simpleui debe colocarse antes de django.contrib.admin. Esto permite que simpleui sobrescriba las plantillas de administración predeterminadas de Django.

Python


# settings.py

INSTALLED_APPS =



1.3 Punto Crítico: Análisis de Compatibilidad de Versiones

Un requisito fundamental del usuario es "evitar incompatibilidades". El análisis de la documentación disponible revela que este es el mayor riesgo del proyecto, no debido a una configuración incorrecta, sino a la falta de una matriz de compatibilidad clara y accesible.
La investigación de la documentación oficial 6 identificó un enlace a un archivo VERSION.md en GitHub que supuestamente contiene la lista de versiones soportadas.6 Sin embargo, los intentos de acceder a este recurso fallaron, resultando inaccesible.7 Del mismo modo, los intentos de extraer los "Clasificadores" de versiones desde el repositorio de paquetes de PyPI (que normalmente lista las versiones de Python y Django compatibles) no arrojaron resultados.8
Dada esta ausencia de documentación oficial sobre compatibilidad, se establece la siguiente recomendación de mitigación como un paso de diligencia debida obligatorio para el desarrollador:
Acción de Mitigación Recomendada:
Antes de integrar django-simpleui en un proyecto, especialmente en entornos de producción, el desarrollador debe verificar manualmente la compatibilidad de la última versión del paquete.
Navegue a la página oficial del proyecto en PyPI: https://pypi.org/project/django-simpleui/
En la barra lateral izquierda, localice la sección Classifiers (Clasificadores).
Examine esta lista para identificar las versiones de Python y Django soportadas explícitamente por el mantenedor del paquete. Busque líneas como:
Programming Language :: Python :: 3.x
Framework :: Django :: 4.x (o las versiones específicas que correspondan).
Ignorar este paso y asumir la compatibilidad con las últimas versiones de Django o Python es el principal riesgo que puede llevar a fallos funcionales o estéticos.

Sección II: Configuración Esencial y Estética (Temas)

Esta sección cubre los parámetros básicos para activar simpleui y controlar su apariencia general, abordando el requisito de "no perder estética".

2.1 Activación y Selección de Tema

El parámetro de configuración principal para definir la apariencia de la interfaz es SIMPLEUI_DEFAULT_THEME.
Esta variable se establece en settings.py y especifica el nombre del archivo CSS que se utilizará como tema. La ruta de este archivo es relativa al directorio simpleui/theme dentro del paquete instalado.9

Python


# settings.py

# Especifica el tema por defecto de simpleui.
# El valor por defecto, si no se especifica, es 'admin.lte.css'.
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'



2.2 Catálogo de Temas Disponibles

La documentación proporciona una lista de 28 temas disponibles, permitiendo una personalización visual significativa.9 Para usar un tema, se debe especificar su nombre de archivo en SIMPLEUI_DEFAULT_THEME.
La siguiente tabla mapea los nombres descriptivos de los temas (traducidos al español) con sus nombres en inglés y un nombre de archivo .css inferido, basado en el ejemplo admin.lte.css proporcionado en la documentación.9
Nombre del Tema (Español)
Nombre del Tema (Inglés)
Nombre de Archivo .css (Inferido)
Por Defecto
Default
(Valor por defecto)
Simpleui-x
Simpleui-x
simpleui-x.css
Element-UI
Element-UI
element-ui.css
layui
layui
layui.css
Ant Design Pro
Ant Design Pro
ant.design.pro.css
Admin LTE
Admin LTE
admin.lte.css (Defecto explícito)
Highdmin
Highdmin
highdmin.css
Aeronave
Aircraft
aircraft.css
Púrpura
Purple
purple.css
Gris
Gray
gray.css
Verde Oscuro
Dark green
dark.green.css
Naranja
Orange
orange.css
Negro
Black
black.css
Verde
Green
green.css
Claro
Light
light.css
Azul Empresarial
Enterprise blue
enterprise.blue.css
Azul Empresarial Pro
Enterprise blue pro
enterprise.blue.pro.css
Verde Empresarial
Enterprise green
enterprise.green.css
Verde Empresarial Pro
Enterprise green pro
enterprise.green.pro.css
Rojo Empresarial
Enterprise red
enterprise.red.css
Rojo Empresarial Pro
Enterprise red pro
enterprise.red.pro.css
Púrpura Empresarial
Enterprise purple
enterprise.purple.css
Púrpura Empresarial Pro
Enterprise purple pro
enterprise.purple.pro.css
Negro Empresarial
Enterprise black
enterprise.black.css
Negro Empresarial Pro
Enterprise black pro
enterprise.black.pro.css
x-verde
x-green
x-green.css
x-rojo
x-red
x-red.css
x-azul
x-blue
x-blue.css


2.3 Despliegue en Entornos Offline (Intranet)

Este es un parámetro funcional crítico para proyectos que no tienen acceso a la red pública de Internet, como aplicaciones de intranet corporativas o servidores seguros.
El parámetro es SIMPLEUI_STATIC_OFFLINE (válido desde la versión 2.1.3 o superior).9
Valor por defecto: False
Por defecto, simpleui carga sus recursos estáticos (CSS, JS) desde CDNs de terceros. Si el servidor o el cliente no tienen acceso a Internet, la interfaz de administración fallará en cargarse correctamente, resultando en una pérdida total de estética y funcionalidad.
Configuración para Intranet: True
Al establecer este valor en True, se le indica a simpleui que cargue todos los recursos estáticos desde el servidor local de Django (es decir, los archivos servidos a través de collectstatic).

Python


# settings.py

# OBLIGATORIO para despliegues en intranet o sin acceso a Internet.
# Fuerza la carga de todos los recursos estáticos localmente.
SIMPLEUI_STATIC_OFFLINE = True



2.4 Ajustes Menores de la Interfaz (Carga y Login)

simpleui incluye dos parámetros para controlar elementos estéticos menores:
SIMPLEUI_LOADING (Válido desde la v2.1.5+):
Propósito: Controla la máscara de carga (animación "loading") que aparece al navegar entre páginas en el admin.
Valores: True (predeterminado) la muestra. False la oculta.9
Uso: SIMPLEUI_LOADING = False
SIMPLEUI_LOGIN_PARTICLES:
Propósito: Controla la animación de partículas de fondo en la página de inicio de sesión (/admin/login/).
Valores: True (predeterminado) la activa. False la desactiva, dejando un fondo limpio.9
Uso: SIMPLEUI_LOGIN_PARTICLES = False

Sección III: Arquitectura de Configuración y Personalización de Marca (Branding)

Una de las principales fuentes de confusión al configurar simpleui es su arquitectura de configuración fragmentada. Los parámetros no se encuentran en un único diccionario unificado. Comprender esta estructura es esencial para una configuración correcta.

3.1 La Arquitectura de Configuración de 3 Niveles

El análisis de todos los parámetros disponibles 9 revela una estructura de configuración de tres niveles distintos, todos coexistiendo en settings.py:
Nivel 1: Parámetros Globales (Variables Simples)
Son variables de nivel superior en settings.py que controlan configuraciones globales de branding y homepage. Ejemplos: SIMPLEUI_LOGO, SIMPLEUI_HOME_PAGE. (Cubiertos en esta sección).
Nivel 2: Diccionario de Iconos (Mapeo Simple)
Un diccionario de nivel superior llamado SIMPLEUI_ICON usado para un mapeo rápido de iconos a aplicaciones existentes sin alterar la estructura del menú.9 (Cubierto en la Sección IV).
Nivel 3: Diccionario de Configuración (Estructura Avanzada)
Un diccionario de nivel superior llamado SIMPLEUI_CONFIG que controla la reestructuración avanzada de menús, el orden, el filtrado y el comportamiento dinámico.9 (Cubierto en la Sección V).
Los intentos de verificar si los parámetros de Nivel 1 (como SIMPLEUI_LOGO o SIMPLEUI_HOME_PAGE) podían anidarse dentro del Nivel 3 (SIMPLEUI_CONFIG) fallaron, confirmando que son sistemas separados.9

3.2 Configuración del Logo e Identidad (Nivel 1)

Estos parámetros globales de Nivel 1 controlan la identidad visual básica del panel de administración.
SIMPLEUI_LOGO
Propósito: Reemplaza el logo por defecto de SimpleUI.
Valor: Una cadena de texto (string) que contiene la URL (absoluta) de la imagen del logo.9
Ejemplo: SIMPLEUI_LOGO = 'https://miempresa.com/logo-admin.png'
SIMPLEUI_INDEX
Propósito: Define la dirección a la que se redirige al usuario al hacer clic en el logo/icono de inicio en la parte superior de la página.
Valor por Defecto: '/' (la raíz del sitio).
Uso: Puede establecerse como una ruta relativa (ej. '/mi-dashboard/') o una URL absoluta (ej. 'https://miempresa.com'). Si se usa una URL absoluta, se abrirá en una nueva pestaña (window.open).9
Ejemplo: SIMPLEUI_INDEX = 'https://miempresa.com'

3.3 Personalización de la Página de Inicio (Nivel 1)

Estos parámetros de Nivel 1 permiten reemplazar completamente la página de inicio (dashboard) predeterminada de simpleui con una página externa, como un dashboard de BI (Business Intelligence) o una URL personalizada.
SIMPLEUI_HOME_PAGE
Propósito: Si se establece, la página de inicio del admin se convierte en un iframe que carga la URL especificada. La página de inicio por defecto de simpleui (con acciones recientes, etc.) se ignora.9
Valor: La URL de la página a incrustar.
Ejemplo: SIMPLEUI_HOME_PAGE = 'https://mi-dashboard.grafana.net'
SIMPLEUI_HOME_TITLE
Propósito: Establece el título de la página de inicio (visible en el menú de navegación).9
Valor: Una cadena de texto.
Ejemplo: SIMPLEUI_HOME_TITLE = 'Dashboard de Analíticas'
SIMPLEUI_HOME_ICON
Propósito: Establece el icono de la página de inicio en el menú. Admite clases de FontAwesome y Element-UI.9
Valor: Una cadena de texto con la clase del icono.
Ejemplo: SIMPLEUI_HOME_ICON = 'fa fa-chart-bar'

3.4 Control de Módulos de la Página de Inicio (Nivel 1)

Si no se utiliza un SIMPLEUI_HOME_PAGE personalizado, simpleui muestra un dashboard por defecto con tres módulos. Estos parámetros de Nivel 1 permiten ocultarlos individualmente.9 Esto también es útil si se usa un SIMPLEUI_HOME_PAGE para evitar que los módulos predeterminados aparezcan brevemente o interfieran.
SIMPLEUI_HOME_INFO
Propósito: Controla la visibilidad del módulo "Información del Servidor".
Valores: True (predeterminado) para mostrar, False para ocultar.
Uso: SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK
Propósito: Controla la visibilidad del módulo "Acciones Rápidas".
Valores: True (predeterminado) para mostrar, False para ocultar.
Uso: SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION
Propósito: Controla la visibilidad del módulo "Acciones Recientes" (Logs de admin).
Valores: True (predeterminado) para mostrar, False para ocultar.
Uso: SIMPLEUI_HOME_ACTION = False

Sección IV: Configuración de Iconos (Enfoques Simple y Avanzado)

La personalización de iconos es fundamental para la estética y utiliza dos de los niveles de arquitectura de configuración: Nivel 1 (para un ajuste global) y Nivel 2 o 3 (para asignaciones específicas). La documentación indica que los iconos se basan en FontAwesome.9

4.1 Enfoque 1 (Simple): Mapeo Rápido con SIMPLEUI_ICON (Nivel 2)

Este es el Nivel 2 de la arquitectura de configuración. Se utiliza un diccionario SIMPLEUI_ICON en settings.py para asignar rápidamente iconos a las aplicaciones (módulos) existentes, sin necesidad de reestructurar todo el menú.
La clave del diccionario es el nombre visible de la aplicación en el menú (tal como Django lo genera, ej. 'Autenticación y autorización' o el verbose_name de la AppConfig), y el valor es la clase completa del icono de FontAwesome.9
Sintaxis 9:

Python


# settings.py

# Nivel 2: Mapeo simple de iconos
SIMPLEUI_ICON = {
    'Autenticación y autorización': 'fas fa-user-shield',
    'Gestión de Empleados': 'fas fa-user-tie',
    # (Nombre de la App): (Clase de FontAwesome)
}



4.2 Enfoque 2 (Avanzado): Iconos dentro de SIMPLEUI_CONFIG (Nivel 3)

Este es el Nivel 3. Si se planea reestructurar, renombrar o reordenar los menús utilizando el diccionario SIMPLEUI_CONFIG (ver Sección V), el diccionario SIMPLEUI_ICON (Nivel 2) no debe usarse.
En su lugar, la clave 'icon' se define directamente dentro de la estructura del menú para cada aplicación o modelo que se esté personalizando.9
Sintaxis 9:

Python


# settings.py

# Nivel 3: Configuración avanzada de menú e iconos
SIMPLEUI_CONFIG = {
    'menus':
        }
    ]
}



4.3 Iconos por Defecto (SIMPLEUI_DEFAULT_ICON) (Nivel 1)

Este es un parámetro global de Nivel 1 que controla el comportamiento de los menús que no tienen un icono asignado (ni por defecto del sistema ni mediante los métodos anteriores).
Propósito: Controla si se asigna automáticamente un icono genérico de "archivo" a los elementos del menú que carecen de uno.9
Valores:
True (predeterminado): Se activa el icono de archivo por defecto.
False: Se desactiva el icono de archivo por defecto. Los menús sin icono simplemente no mostrarán uno.
Uso: SIMPLEUI_DEFAULT_ICON = False

Sección V: Guía Maestra de Menús (SIMPLEUI_CONFIG)

Esta es la característica más potente y compleja de simpleui, correspondiente al Nivel 3 de la arquitectura de configuración. El diccionario SIMPLEUI_CONFIG permite un control total sobre la estructura, el contenido y el comportamiento de la barra de navegación lateral.

5.1 El Diccionario SIMPLEUI_CONFIG

La estructura base del diccionario SIMPLEUI_CONFIG en settings.py contiene claves para el control global (system_keep, menu_display, dynamic) y una clave para la estructura del menú (menus).9

Python


# settings.py
import time  # Requerido si se usan menús dinámicos 

SIMPLEUI_CONFIG = {
    # --- Claves de Control Global ---
    
    # ¿Conservar los menús del sistema (ej. auth)?
    # False (defecto) = Ocultar menús del sistema si 'menus' está definido.
    # True = Mostrar menús personalizados Y menús del sistema.
    'system_keep': False, 
    
    # Habilita el filtrado y ordenamiento del menú.
    # Si se define, solo se muestran los 'name' de esta lista, en este orden.
    # Una lista vacía oculta TODOS los menús.
    'menu_display':,
    
    # ¿Regenerar el menú en CADA inicio de sesión?
    # ADVERTENCIA: Impacta el rendimiento.
    'dynamic': False,
    
    # --- Clave de Estructura de Menú ---
    'menus': [
        #... Aquí se definen las estructuras de menú...
    ]
}



5.2 Claves de Control Global

Estas claves, ubicadas en la raíz de SIMPLEUI_CONFIG, definen el comportamiento general del menú.9
system_keep
Propósito: Controla si los menús predeterminados de Django (como 'Autenticación y autorización') coexisten con los menús personalizados definidos en la clave 'menus'.
Valores: False (predeterminado) oculta los menús del sistema si se define 'menus'. True los muestra a ambos.9
menu_display
Propósito: Filtra y ordena los menús de nivel superior.
Valor: Una lista de cadenas (list). Cada cadena debe coincidir exactamente con el valor de la clave 'name' de un menú de nivel superior.
Comportamiento: Si la lista no está vacía, solo se mostrarán los menús cuyos nombres estén en la lista, y aparecerán en el orden exacto de la lista. Si la lista está vacía (``), no se mostrará ningún menú.9
dynamic
Propósito: Activa la regeneración dinámica de menús.
Valores: False (predeterminado). Si se establece en True, simpleui volverá a leer esta configuración en cada inicio de sesión del usuario. Esto permite menús que cambian con el tiempo 9` en un nombre).9
Advertencia de Rendimiento: La documentación advierte explícitamente que establecer dynamic = True "causará una sobrecarga adicional", ya que el archivo de configuración se vuelve a leer en cada acceso al admin. Usar con precaución.9

5.3 Anatomía de la Estructura menus

La clave 'menus' es una lista de diccionarios. Cada diccionario representa un elemento del menú de nivel superior (generalmente una aplicación de Django o un grupo personalizado). El ejemplo en la documentación 9 ilustra varios casos de uso.
Caso 1: Agrupar una App de Django (ej. 'auth')
Esto toma la aplicación auth de Django, la renombra, le da un icono y define cuáles de sus modelos mostrar.

Python


{
    'app': 'auth',  # El nombre interno de la app en Django
    'name': 'Autenticación de Permisos', # Nuevo nombre visible
    'icon': 'fas fa-user-shield',
    'models':
}


Caso 2: Crear un Menú de Enlace Externo
Esto crea un elemento de menú que no está vinculado a una aplicación de Django, sino a una URL externa.9

Python


{
    'name': 'Documentación Simpleui',
    'icon': 'fas fa-code',
    'url': 'https://newpanjing.github.io/simpleui_docs/',
    'newTab': True  # Importante: abre el enlace en una nueva pestaña
}


Caso 3: Crear Menús Anidados (Multinivel)
simpleui permite menús de tres niveles. Esto se logra anidando diccionarios usando la clave 'models' recursivamente.9

Python


{
    'name': 'Menú Multinivel',
    'icon': 'fa fa-file',
    'models':
        },
        {
            'name': 'Submenú 2 (Enlace)',
            'url': 'https://...',
            'icon': 'fab fa-github'
        }
    ]
}



5.4 Tabla de Claves de Configuración de menus

La siguiente tabla resume las claves disponibles para los diccionarios dentro de la lista 'menus', según el análisis de.9
Clave
Obligatorio
Propósito
Nivel
name
Sí
El texto visible del elemento del menú.
App / Modelo
icon
No
Clase de FontAwesome (ej. fa fa-user).
App / Modelo
app
Opcional
El nombre de la app de Django (ej. auth). Usado para agrupar modelos de esa app.
App (Nivel 1)
models
Opcional
Una lista de diccionarios de sub-menú o modelo.
App / Modelo
url
Opcional
Enlace relativo al admin (ej. auth/user/) o absoluto (https://...).
Modelo
newTab
No
Si es True, la url se abre en una nueva pestaña.
Modelo


Sección VI: Consideraciones Adicionales y Privacidad

Esta sección cubre parámetros que no encajan en las categorías anteriores pero que son vitales para el cumplimiento y la gobernanza del proyecto.

6.1 Gestión de la Privacidad (SIMPLEUI_ANALYSIS)

Por defecto, django-simpleui recopila datos de análisis de uso. La documentación indica que esto se hace para mejorar el proyecto, que se informa una vez al día y que "no lee información sensible".9
Sin embargo, en entornos corporativos, regulados (como GDPR) o de alta seguridad, cualquier recopilación de datos de terceros no solicitada es una preocupación de cumplimiento y privacidad.
Parámetro: SIMPLEUI_ANALYSIS
Valor por Defecto: True (Recopilación de análisis activada).
Acción Recomendada: Para garantizar la privacidad y el cumplimiento, se recomienda encarecidamente desactivar esta función.

Python


# settings.py

# Desactiva la recopilación de datos de análisis de uso.
SIMPLEUI_ANALYSIS = False



Sección VII: Referencia Completa de Parámetros

Esta sección final consolida todos los parámetros de configuración identificados en la documentación 9 en una única tabla de referencia maestra.
Parámetro (en settings.py)
Tipo (Inferido)
Descripción (Español)
Valor por Defecto
SIMPLEUI_LOGIN_PARTICLES
bool
Activa/Desactiva la animación de partículas del login.
True
SIMPLEUI_DEFAULT_THEME
str
Especifica el archivo .css del tema.
'admin.lte.css'
SIMPLEUI_HOME_PAGE
str
URL para incrustar como página de inicio (iframe).
(Ninguno)
SIMPLEUI_HOME_TITLE
str
Título de la página de inicio personalizada.
(Ninguno)
SIMPLEUI_HOME_ICON
str
Icono (FontAwesome/Element-UI) para la página de inicio.
(Ninguno)
SIMPLEUI_INDEX
str
URL a la que enlaza el logo/icono de inicio.
'/'
SIMPLEUI_HOME_INFO
bool
Muestra/Oculta el módulo "Información del Servidor".
True
SIMPLEUI_HOME_QUICK
bool
Muestra/Oculta el módulo "Acciones Rápidas".
True
SIMPLEUI_HOME_ACTION
bool
Muestra/Oculta el módulo "Acciones Recientes".
True
SIMPLEUI_LOGO
str
URL del logo personalizado.
(Ninguno)
SIMPLEUI_ANALYSIS
bool
Permite/Bloquea la recopilación de datos de análisis.
True
SIMPLEUI_STATIC_OFFLINE
bool
True para cargar estáticos localmente (intranet).
False
SIMPLEUI_LOADING
bool
Muestra/Ocula la máscara de carga global.
True
SIMPLEUI_DEFAULT_ICON
bool
Asigna un icono de "archivo" por defecto a menús sin icono.
True
SIMPLEUI_ICON
dict
(Nivel 2) Diccionario para mapeo simple de iconos: {'App': 'fa...'}.
{}
SIMPLEUI_CONFIG
dict
(Nivel 3) Diccionario para reestructuración avanzada de menús.
{}
SIMPLEUI_CONFIG['system_keep']
bool
True para conservar menús de sistema.
False
SIMPLEUI_CONFIG['menu_display']
list
Lista para filtrar y ordenar menús.
(Ninguno)
SIMPLEUI_CONFIG['dynamic']
bool
True para regenerar menús en cada login (costoso).
False
SIMPLEUI_CONFIG['menus']
list
Lista de diccionarios que define la estructura del menú.
``

Fuentes citadas
Django SimpleUI, acceso: noviembre 12, 2025, https://newpanjing.github.io/simpleui_docs/
django-simpleui · GitHub Topics, acceso: noviembre 12, 2025, https://github.com/topics/django-simpleui
newpanjing/simplepro: Simple UI pro professional version simple UI front and rear end separation, more functions, more beautiful interface!Simple UI Pro 专业版simple UI 前后端分离，功能更多界面更美观！ - GitHub, acceso: noviembre 12, 2025, https://github.com/newpanjing/simplepro
django-simpleui - PyPI, acceso: noviembre 12, 2025, https://pypi.org/project/django-simpleui/2024.4.1/
django-simpleui - PyPI, acceso: noviembre 12, 2025, https://pypi.org/project/django-simpleui/3.0/
newpanjing/simpleui: A modern theme based on vue+ ... - GitHub, acceso: noviembre 12, 2025, https://github.com/newpanjing/simpleui
acceso: diciembre 31, 1969, https://github.com/newpanjing/simpleui/blob/master/VERSION.md
django-simpleui · PyPI, acceso: noviembre 12, 2025, https://pypi.org/project/django-simpleui/
快速上手指南| Django SimpleUI, acceso: noviembre 12, 2025, https://newpanjing.github.io/simpleui_docs/config.html
