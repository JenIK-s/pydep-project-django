from django import template

register = template.Library()


@register.filter
def pluralize_months(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return f'{value} месяцев'

    if value % 10 == 1 and value % 100 != 11:
        suffix = 'месяц'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        suffix = 'месяца'
    else:
        suffix = 'месяцев'
    return f'{value} {suffix}'


@register.filter
def pluralize_lessons(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return f'{value} уроков'

    if value % 10 == 1 and value % 100 != 11:
        suffix = 'урок'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        suffix = 'урока'
    else:
        suffix = 'уроков'
    return f'{value} {suffix}'
