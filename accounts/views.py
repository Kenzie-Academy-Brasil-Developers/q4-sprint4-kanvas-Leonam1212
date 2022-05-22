from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from accounts.permissions import Authenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY
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
from accounts.serializers import AccountsSerializer, LoginSerializer

# Create your views here.

class AccountsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Authenticated]

    def get(self, request: Request):
        users = Accounts.objects.all()
        serializer = AccountsSerializer(users, many=True)

        return Response(serializer.data, HTTP_200_OK)

    def post(self, request: Request):
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_user = Accounts.objects.filter(
            email=serializer.validated_data["email"]
        ).exists()

        if found_user:
            return Response({"message": "User already exists"}, HTTP_422_UNPROCESSABLE_ENTITY)

        user = Accounts.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()

        serializer = AccountsSerializer(user)

        return Response(serializer.data, HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )

    if not user:
        return Response({"message": "Invalid credential."}, HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key})


# @api_view(["GET"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_users_view(request: Request):
#     print("aqui")
#     users = Accounts.objects.all()
#     serializer = AccountsSerializer(users, many=True)

#     return Response(serializer.data, HTTP_200_OK)
