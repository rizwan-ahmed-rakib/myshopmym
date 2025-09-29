from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Cart


class CartInline(admin.TabularInline):
    model = Order.orderitems.through
    extra = 0
    readonly_fields = ("product_image", "product_name", "quantity", "total_price")

    def product_image(self, obj):
        try:
            product = obj.cart.item
            if product.mainimage:
                return format_html(
                    '<img src="{}" style="width:60px; height:60px; object-fit:cover;" />',
                    product.mainimage.url
                )
        except:
            return "No Image"
        return "No Image"

    product_image.short_description = "Image"

    def product_name(self, obj):
        return obj.cart.item.name if obj.cart and obj.cart.item else "N/A"

    def quantity(self, obj):
        return obj.cart.quantity if obj.cart else "N/A"

    def total_price(self, obj):
        return obj.cart.get_total() if obj.cart else "N/A"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "colored_status", "order_type_display",
        "delivery_type_display", "created", "order_preview_images", "get_totals"
    )
    list_filter = ("status", "order_type", "delivery_type", "created")
    search_fields = (
        "user__username", "receiver_name", "receiver_email", "receiver_phone_number"
    )
    inlines = [CartInline]

    # ✅ Display label instead of raw choice
    def order_type_display(self, obj):
        return obj.get_order_type_display()

    order_type_display.short_description = "Payment Method"

    def delivery_type_display(self, obj):
        return obj.get_delivery_type_display()

    delivery_type_display.short_description = "Delivery Type"

    # ✅ Status with color
    def colored_status(self, obj):
        color_map = {
            "PENDING": "red",
            "PROCESSING": "orange",
            "ONGOING": "blue",
            "COMPLETED": "green",
            "CANCELLED": "gray",
        }
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color_map.get(obj.status, "black"),
            obj.get_status_display()
        )

    colored_status.short_description = "Status"

    def order_preview_images(self, obj):
        images_html = ""
        for cart_item in obj.orderitems.all():
            if cart_item.item and cart_item.item.mainimage:
                images_html += f'<img src="{cart_item.item.mainimage.url}" style="width:50px; height:50px; object-fit:cover; margin-right:4px; border-radius:4px;" />'
        return format_html(images_html) if images_html else "No Images"

    order_preview_images.short_description = "Product Images"

    # ✅ Highlight new orders (less than 1 day old)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-created")  # latest first


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
