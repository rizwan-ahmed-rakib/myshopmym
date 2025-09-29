from django.db import models
from django.conf import settings
from shop_app.models import Product


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}---{self.user}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total





class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    DELIVERY_TYPE_CHOICES = [
        ("STORE_PICKUP", "Store Pickup"),
        ("HOME_DELIVERY", "Home Delivery"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),  # Order just placed
        ("PROCESSING", "Processing"),  # Order is being prepared
        ("ONGOING", "On the way"),  # Delivery ongoing
        ("COMPLETED", "Completed"),  # Order delivered
        ("CANCELLED", "Cancelled"),  # Order cancelled
    ]

    orderitems = models.ManyToManyField("Cart")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE_CHOICES, default="COD"
    )  # ✅ Cash on delivery or Online payment

    delivery_type = models.CharField(
        max_length=20, choices=DELIVERY_TYPE_CHOICES, default="HOME_DELIVERY"
    )  # ✅ Pickup or Home Delivery

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )  # ✅ Current status of order

    receiver_phone_number = models.CharField(max_length=20)  # ✅ Delivery phone
    receiver_address = models.TextField()  # ✅ Delivery address
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_email = models.EmailField()
    receiver_city = models.CharField(max_length=100, blank=True, null=True)
    receiver_zip_code = models.CharField(max_length=10, blank=True, null=True)
    receiver_country = models.CharField(max_length=100, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user} -> {self.status} -> {self.created.strftime('%Y-%m-%d %H:%M')}"



    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total
    class Meta:
        ordering = ['-created', ]
