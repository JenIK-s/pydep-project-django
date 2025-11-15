from django.core.paginator import Paginator
from django.conf import settings


def paginator(request, name):
    create_paginator = Paginator(name, settings.COUNT_POSTS)
    page_number = request.GET.get('page')
    page_obj = create_paginator.get_page(page_number)

    return page_obj
