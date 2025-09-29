from rest_framework import serializers
from .models import Cart, Order
from shop_app.models import Product


class CartSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2, read_only=True)
    total = serializers.SerializerMethodField()
    product_image = serializers.ImageField(source='item.mainimage', read_only=True)


    class Meta:
        model = Cart
        fields = [
            'id',
            # 'user',
            'item',
            'item_name',
            'item_price',
            'quantity',
            'purchased',
            'created',
            'updated',
            'total',
            'product_image',
        ]
        read_only_fields = [ 'purchased', 'created', 'updated', 'total']

    def get_total(self, obj):
        return obj.get_total()


class OrderSerializer(serializers.ModelSerializer):
    orderitems = CartSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    product_image = serializers.ImageField(source='item.mainimage', read_only=True)

    class Meta:
        model = Order
        # fields = [
        #     'id',
        #     'user',
        #     'orderitems',
        #     'ordered',
        #     'created',
        #     'paymentId',
        #     'orderId',
        #     'total',
        #     'product_image',
        # ]

        fields = [
            'id',
            'user',
            'orderitems',
            'product_image',
            'order_type',
            'delivery_type',
            'status',
            'receiver_phone_number',
            'receiver_address',
            'receiver_name',
            'receiver_email',
            'receiver_city',
            'receiver_zip_code',
            'receiver_country',
            'ordered',
            'created',
            'paymentId',
            'orderId',
            'total',
        ]

        read_only_fields = ['user', 'ordered', 'created', 'total']

    def get_total(self, obj):
        return obj.get_totals()
