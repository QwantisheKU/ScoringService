from .models import Calculation
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate_calculations(request, calculations, results):

    page = request.GET.get('page')
    paginator = Paginator(calculations, results)
    try:
        calculations = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        calculations = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        calculations = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, calculations
