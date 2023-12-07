from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('addRestaurent/',addRestaurent),
    path('forget-password/',send_otp)
]
