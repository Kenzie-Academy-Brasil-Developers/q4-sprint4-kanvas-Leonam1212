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
        serializer =  AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def put_address_view(request: Request):
    serializer = AddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.users_id = request.user.uuid
    print(serializer)
    address = Address.objects.create(**serializer.validated_data)


    return Response(address, HTTP_200_OK)
