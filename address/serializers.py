from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    zip_code = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
