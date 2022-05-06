from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
