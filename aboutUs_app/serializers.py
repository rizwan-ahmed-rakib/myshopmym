from rest_framework import serializers
from .models import Setup_page, SliderBanners, ContactInfo, ContactMessage


class Setup_page_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Setup_page
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderBanners
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
