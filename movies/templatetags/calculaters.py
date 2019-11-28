from django import template
register = template.Library()

@register.filter
def div( value ):
    return range(value//2)

@register.filter
def remainder( value ):
    if value%2:
        return range(1)
    else:
        return range(0)

@register.filter
def empty( value ):
    if value%2:
        return range(4 - value//2)
    else:
        return range(5 - value//2)

@register.filter
def star( value ):
    return range(value)

@register.filter
def empty_star( value ):
    return range(5-value)
