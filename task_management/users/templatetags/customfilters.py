from django import template
from datetime import datetime
from django.utils import timezone
register = template.Library()

# Example filter: capitalize first letter
@register.filter
def capitalize_first(value):
    if isinstance(value, str) and value:
        return value[0].upper() + value[1:]
    return value

@register.filter
def format_date(value):
    if value:
        today = datetime.now().date()
        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        return value.strftime('%B %d, %Y')
    return "N/A"