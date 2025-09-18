from .models import Category

# def categories_processor(request):
#     return {
#         'categories': Category.objects.all()
#     }


def categories_processor(request):
    return {
        # শুধু Parent Category গুলো global context এ যাবে
        # 'categories': Category.objects.filter(parent__isnull=True)
        'categories': Category.objects.filter(parent=None)

    }
