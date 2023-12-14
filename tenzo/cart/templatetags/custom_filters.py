from django import template

register = template.Library()

@register.filter(name='quantity_filter')
def get_value(dictionary, key):
    return dictionary.get(str(key), 0)