from django.urls import path

from address.views import AddressView, put_address_view

urlpatterns = [
    path("address/", put_address_view)
]
