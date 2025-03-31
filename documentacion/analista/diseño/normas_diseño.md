# Normas de Diseño - Sistema Reloj Fichador

## Introducción

Este documento establece las pautas de diseño que deben seguirse en el desarrollo y mantenimiento del Sistema Reloj Fichador. Estas normas garantizan la coherencia visual y funcional en todas las interfaces y componentes del sistema.

## 1. Paleta de Colores

### 1.1 Colores Primarios
- **Azul corporativo**: `#3498DB` - Color principal para elementos destacados
- **Gris oscuro**: `#2C3E50` - Textos principales y encabezados
- **Blanco**: `#FFFFFF` - Fondos principales

### 1.2 Colores Secundarios
- **Azul oscuro**: `#34495E` - Cabeceras de tablas y barras de navegación
- **Gris claro**: `#BDC3C7` - Bordes y elementos secundarios
- **Gris medio**: `#7F8C8D` - Textos secundarios e información adicional

### 1.3 Colores de Acento
- **Verde**: `#27AE60` - Éxito y confirmación
- **Rojo**: `#E74C3C` - Error y alertas
- **Amarillo**: `#F39C12` - Advertencias
- **Morado**: `#8E44AD` - Destacados secundarios

## 2. Tipografía

### 2.1 Fuentes
- **Texto principal**: Helvetica (o Arial como alternativa)
- **Texto secundario**: Helvetica (o Arial como alternativa)
- **Código**: Consolas, Monaco o monoespaciada predeterminada

### 2.2 Tamaños
- **Títulos principales**: 20px, negrita
- **Subtítulos**: 16px, negrita
- **Texto normal**: 12px, normal
- **Texto pequeño**: 10px, normal
- **Encabezados de tabla**: 10px, negrita

### 2.3 Estilos
- **Encabezados**: Alineados a la izquierda, con espacio inferior de 10px
- **Párrafos**: Alineados a la izquierda, interlineado de 1.2
- **Enlaces**: Color azul corporativo, sin subrayado excepto al pasar el cursor

## 3. Componentes UI

### 3.1 Botones
- **Botones primarios**: Fondo azul corporativo, texto blanco, bordes redondeados (4px)
- **Botones secundarios**: Borde gris claro, texto gris oscuro, fondo blanco
- **Botones de acción negativa**: Fondo rojo, texto blanco
- **Tamaño estándar**: Padding vertical 8px, horizontal 12px

### 3.2 Formularios
- **Campos de entrada**: Borde gris claro (1px), padding 8px, esquinas redondeadas (4px)
- **Etiquetas**: Ubicadas encima de los campos, texto gris oscuro, tamaño 12px
- **Mensajes de error**: Texto rojo, debajo del campo, tamaño 10px
- **Campos obligatorios**: Marcados con asterisco rojo

### 3.3 Tablas
- **Cabeceras**: Fondo azul oscuro, texto blanco, alineación centrada
- **Filas alternas**: Fondo blanco/gris muy claro para mejorar legibilidad
- **Bordes**: Color gris claro, grosor 0.5px
- **Padding de celdas**: 8px

### 3.4 Tarjetas y Paneles
- **Bordes**: Radio de esquina 4px, sombra sutil
- **Padding interno**: 15px
- **Separación entre componentes**: Margen de 20px
- **Títulos**: Parte superior, alineados a la izquierda, texto gris oscuro

## 4. Iconografía

### 4.1 Estilo
- Utilizar el conjunto de iconos Font Awesome 5
- Tamaño consistente (16px por defecto)
- Color que contraste adecuadamente con el fondo

### 4.2 Iconos Comunes
- **Añadir**: fa-plus
- **Editar**: fa-edit
- **Eliminar**: fa-trash
- **Guardar**: fa-save
- **Buscar**: fa-search
- **Configuración**: fa-cog
- **Usuario**: fa-user
- **Cerrar**: fa-times
- **Aceptar**: fa-check
- **Reloj**: fa-clock

## 5. Layout y Estructura

### 5.1 Navegación
- Barra de navegación superior fija
- Menú lateral colapsable en pantallas pequeñas
- Migas de pan (breadcrumbs) para navegación jerárquica

### 5.2 Grilla
- Sistema de 12 columnas
- Márgenes laterales responsivos (40px en escritorio, 20px en tablets)
- Separación entre elementos de 20px

### 5.3 Adaptabilidad
- Puntos de ruptura:
  - Móvil: ≤ 768px
  - Tablet: 769px - 1024px
  - Escritorio: ≥ 1025px
- Elementos deben adaptarse proporcionalmente a cada tamaño

## 6. Feedback al Usuario

### 6.1 Mensajes
- **Éxito**: Fondo verde claro, texto verde oscuro, icono de verificación
- **Error**: Fondo rojo claro, texto rojo oscuro, icono de advertencia
- **Información**: Fondo azul claro, texto azul oscuro, icono de información
- **Advertencia**: Fondo amarillo claro, texto marrón, icono de precaución

### 6.2 Indicadores de Estado
- **Carga**: Animación de spinner con texto "Cargando..."
- **Progreso**: Barra horizontal con porcentaje visible
- **Botones deshabilitados**: Opacidad reducida (0.5)
- **Elementos activos**: Borde o highlight azul corporativo

## 7. Buenas Prácticas de Accesibilidad

- Contraste adecuado entre texto y fondo (ratio mínimo 4.5:1)
- Texto alternativo para imágenes (atributo alt)
- Estructura jerárquica de encabezados (h1, h2, h3...)
- Etiquetas explícitas para campos de formulario
- Mensajes de error claros y específicos
- Elementos interactivos con tamaño mínimo de 44x44px
- Navegación posible con teclado

## 8. Implementación Específica

### 8.1 Frameworks y Librerías
- Bootstrap 4 como base para el sistema de grillas y componentes
- jQuery para interacciones JavaScript básicas
- DataTables para tablas complejas con ordenación y filtrado
- Select2 para selectores avanzados con búsqueda

### 8.2 Nomenclatura CSS
- Usar metodología BEM (Block Element Modifier)
- Prefijo "rf-" para todas las clases específicas del sistema (ej: rf-header)
- Nombres en inglés, minúsculas, separados por guiones

## 9. Plantillas y Componentes

El sistema debe utilizar plantillas estandarizadas para mantener la coherencia:

### 9.1 Plantilla Base
- Cabecera con logo y menú de navegación
- Área de contenido principal
- Pie de página con información de copyright y versión

### 9.2 Formularios Estándar
- Formulario de entrada/salida
- Formularios CRUD para entidades principales
- Filtros de búsqueda y reportes

## 10. Ejemplos y Referencias

Los ejemplos de implementación correcta se encuentran en las siguientes ubicaciones:

- Plantilla de formulario: `templates/reloj_fichador/form_template.html`
- Estilos corporativos: `static/css/reloj_fichador.css`
- Componentes JavaScript: `static/js/components/`

---

Este documento debe revisarse periódicamente para asegurar su vigencia y aplicación en todo el desarrollo del Sistema Reloj Fichador.

*Última actualización: Fecha actual* 