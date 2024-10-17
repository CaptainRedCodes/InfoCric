from django import template
from django.forms.widgets import CheckboxInput

register = template.Library()

@register.filter(name='add_classes')
def add_classes(field, css_classes):
    return field.as_widget(attrs={"class": css_classes})

@register.filter(name='is_checkbox')
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)

@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__

@register.filter(name='placeholder')
def placeholder(field, text):
    field.field.widget.attrs['placeholder'] = text
    return field