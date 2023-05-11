from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def timesince_hours(value):
    # Calculate the time elapsed using the built-in timesince function
    time_elapsed = timesince(value)

    # Split the time elapsed string into separate parts
    parts = time_elapsed.split(", ")

    # If there are minutes in the time elapsed string, remove them
    if len(parts) == 1:
        parts.pop()

    # Join the parts back together and return the modified string
    return ", ".join(parts)
