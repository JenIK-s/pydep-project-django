from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def get_weekday(day):
    year = datetime.today().year
    month = datetime.today().month
    date_string = f"{year}-{month:02d}-{day:02d}"
    date = datetime.strptime(date_string, "%Y-%m-%d")
    weekday_name = date.strftime("%A")

    return weekday_name
