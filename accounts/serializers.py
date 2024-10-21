from rest_framework import serializers
from .models import Address

from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'line_1', 'line_2', 'city', 'state', 'postal_code', 'country', 'full_address']
        read_only_fields = ['user', 'full_address']  #  مشخص کنید که چه فیلدهایی فقط برای خواندن باشند.
