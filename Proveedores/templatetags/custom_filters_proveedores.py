from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})



@register.filter
def estado_nombre(value):
    estados = {
        0: '<span class="estado-pedido">Pedido</span>',
        1: '<span class="estado-parcial">Entregado Parcial</span>',
        2: '<span class="estado-completo">Entregado Completo</span>',
    }
    return mark_safe(estados.get(value, '<span>Desconocido</span>'))