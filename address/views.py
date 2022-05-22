from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_409_CONFLICT

from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from accounts.models import Accounts
from address.models import Address
from address.serializers import AddressSerializer


class AddressView(APIView):
    authentication_classes = [TokenAuthentication]

    def put(self, request: Request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)
        found_zip_code = Address.objects.filter(
            zip_code=serializer.validated_data["zip_code"]
        ).exists()

        if found_zip_code:
            return Response({"message": "Zip code already exists"}, HTTP_409_CONFLICT)

        address = Address.objects.create(**serializer.validated_data)

        request.user.address = address
        request.user.save()
        
        serializer = AddressSerializer(address)

        return Response(serializer.data, HTTP_200_OK)
