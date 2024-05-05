from django import template
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

register = template.Library()

@register.filter
def is_email(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False
