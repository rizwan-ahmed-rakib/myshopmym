from rest_framework import serializers
from .models import BillingAddress


class BillingAddressSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.profile.username", read_only=True)

    class Meta:
        model = BillingAddress
        fields = '__all__'

    #     fields = [
    #         "id",
    #         "user",
    #         "username",
    #         "address",
    #         "zipcode",
    #         "city",
    #         "country",
    #     ]
        read_only_fields = ["user"]
