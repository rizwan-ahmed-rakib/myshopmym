from django.contrib import admin
from shop_app.models import Category, Product

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)


# Custom Admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    # এখানে name আর parent দুইটিই দেখাবে list view তে

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
