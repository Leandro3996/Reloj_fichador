from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter para acceder a valores de diccionarios usando claves dinámicas
    Uso: {{ diccionario|lookup:clave }}
    """
    if dictionary and key:
        return dictionary.get(key)
    return None