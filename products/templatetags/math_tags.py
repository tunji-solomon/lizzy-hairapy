from django import template

register = template.Library()

@register.filter
def multiply(a, b):
    try:
        return float(a) * int(b)
    except:
        return ""
    