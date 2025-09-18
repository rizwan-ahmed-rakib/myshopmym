from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'parent',
            'created',
            'image',
            'brand_image',
            'children',
        ]

    def get_children(self, obj):
        """Recursive children fetch"""
        return CategorySerializer(obj.children.all(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'mainimage',
            'image1',
            'image2',
            'image3',
            'name',
            'product_code',
            'category',
            'category_title',
            'preview_text',
            'detail_text',
            'price',
            'old_price',
            'stock_status',
            'created',
        ]
