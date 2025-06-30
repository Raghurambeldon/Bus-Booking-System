from django import template

register = template.Library()

@register.filter
def group_seats(seats, size):
    """
    Groups seats into chunks of `size`
    Usage: {% for row in seats|group_seats:4 %}
    """
    size = int(size)
    return [seats[i:i + size] for i in range(0, len(seats), size)]
