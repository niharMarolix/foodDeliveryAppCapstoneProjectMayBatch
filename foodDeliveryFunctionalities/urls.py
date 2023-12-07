from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('forget-password/',send_otp),
    path('confirm_otp/',confirm_otp),
    path('reset_password/', resetPassword)
]
