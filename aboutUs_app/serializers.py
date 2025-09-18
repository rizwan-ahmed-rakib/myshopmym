from rest_framework import serializers
from .models import Setup_page,SliderBanners

class Setup_page_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Setup_page
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderBanners
        fields = '__all__'
