from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)

from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from accounts.models import Accounts
from accounts.serializers import AccountsSerializer

# Create your views here.


class AccountsView(APIView):

    # def get(self, request: Request):
    #     serializer = AccountsSerializer(request.user)

    #     return Response(serializer.data, HTTP_200_OK)

    def post(self, request: Request):
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_user = Accounts.objects.filter(
            email=serializer.validated_data["email"]
        ).exists()

        if found_user:
            return Response({"message": "User already exists"}, HTTP_409_CONFLICT)

        user = Accounts.object.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()

        serializer = AccountsSerializer(user)

        return Response(serializer.data, HTTP_201_CREATED)
